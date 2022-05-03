"""
Creates a socket tunnel between users localhost to server called RSockServer (Reverse Socket Server) .
Usage:
  client-tunnel.py <client_port>:<instance_name>:<instance_port> <auth>
Takes in the following arguments:
  - client_port: The port that the user can connect to.
  - instance_name: The name of the instance that the user wants to connect to.
  - instance_port: The port that the instance is listening on.
  - auth: The authentication token that the user has to provide to connect to the RSockServer.
  
"""

import os
import ssl
import socket
import threading
from typing import List
from functools import partial
from multiprocessing import Queue
from datetime import datetime, timezone

from nbox.utils import NBOX_HOME_DIR, logger as nbx_logger
from nbox import utils as U
from nbox.auth import secret
from nbox.instance import Instance


class FileLogger:
  def __init__(self, filepath):
    self.filepath = filepath
    self.f = open(filepath, "a")

    self.debug = partial(self.log, level="debug",)
    self.info = partial(self.log, level="info",)
    self.warning = partial(self.log, level="warning",)
    self.error = partial(self.log, level="error",)
    self.critical = partial(self.log, level="critical",)

  def log(self, message, level):
    self.f.write(f"[{datetime.now(timezone.utc).isoformat()}] {level}: {message}\n")
    self.f.flush()


class RSockClient:
  """
  This is a RSockClient. It handels the client socket where client is the user application trying to connect to "client_port"
  Connects to RSockServer listening on localhost:886.
  RSockServer recieves instructions as a string and sends back a response.
  RSockServer requires following steps to setup
  First,
    Authentication:
      - Authentication happens by sending
        `"AUTH~{AUTH_TOKEN}"`
      - AUTH_TOKEN is not defined and is default to 'password'
    Seting config:
      - you can set config by sending
        `"SET_CONFIG~{instance}~{instance_port}"`
      - "instance" - Currently is the internal ip of the instance.
      - "instance_port" - What port users wants to connect to.
    Connect:
      - This Starts the main loop which
        1. Listen on client_port
        2. On connection, 
      2. On connection, 
        2. On connection, 
          a. Send AUTH
          b. If AUTH is successful, send SET_CONFIG
          c. If SET_CONFIG is successful, send CONNECT
          d. If CONNECT is successful, start io_copy
    IO_COPY:
      - This is the main loop that handles the data transfer between client and server. This is done by creating a new thread for each connection.
      - The thread is created by calling the function "io_copy" for each connection that is "server" and "client".
      - When a connection is closed, the loop is stopped.
  """

  def __init__(self, connection_id, client_socket, user, subdomain, instance_port, file_logger, auth, secure=False):
    """
    Initializes the client.
    Args:
      client_socket: The socket that the client is connected to.
      instance: The instance that the client wants to connect to.
      instance_port: The port that the instance is listening on.
      auth: The authentication token that the client has to provide to connect to the RSockServer.
      secure: Whether or not the client is using SSL.
    
    """
    self.connection_id = connection_id
    self.client_socket = client_socket
    self.user = user
    self.subdomain = subdomain
    self.instance_port = instance_port
    self.auth = auth
    self.secure = secure

    self.client_auth = False
    self.rsock_thread_running = False
    self.client_thread_running = False
    self.logger = file_logger

    self.log('Starting client')
    self.connect_to_rsock_server()
    self.log('Connected to RSockServer')
    # self.authenticate()
    # self.log('Authenticated client')
    self.set_config()
    self.log('Client init complete')

  def __repr__(self):
    return f"""RSockClient(
  connection_id={self.connection_id},
  client_socket={self.client_socket},
  user={self.user},
  subdomain={self.subdomain},
  instance_port={self.instance_port},
  auth={self.auth},
)"""
  
  def log(self, message, level=20):
    self.logger.info(f"[{self.connection_id}] [{level}] {message}")
  
  def connect_to_rsock_server(self):
    """
    Connects to RSockServer.
    """
    self.log('Connecting to RSockServer', 10)
    rsock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rsock_socket.connect(('rsock.rc.nimblebox.ai', 886))

    if self.secure:
      self.log('Starting SSL')
      certfile = U.join(U.folder(__file__), "pub.crt")
      self.rsock_socket = ssl.wrap_socket(rsock_socket, ca_certs=certfile, cert_reqs=ssl.CERT_REQUIRED)
    else:
      self.rsock_socket = rsock_socket

  def authenticate(self):
    """
    Authenticates the client.
    Sends `"AUTH~{AUTH_TOKEN}"` to RSockServer.
    """
    self.log('Authenticating client')
    self.rsock_socket.sendall(bytes('AUTH~{}'.format(self.auth), 'utf-8'))
    auth = self.rsock_socket.recv(1024)
    auth = auth.decode('utf-8')
    if auth == 'OK':
      self.log('Client authenticated')
    else:
      self.log('Client authentication failed', 40)
      self.client_auth = False
      exit(1)
  
  def set_config(self):
    """
    Sets the config of the client.
    Sends `"SET_CONFIG~{instance}~{instance_port}"` to RSockServer.
    """
    self.log('Setting config')
    self.rsock_socket.sendall(bytes('SET_CLIENT~{}~{}~{}~{}'.format(self.user, self.subdomain, self.instance_port, self.auth), 'utf-8'))
    config = self.rsock_socket.recv(1024)
    config = config.decode('utf-8')
    self.log('Config set to {}'.format(config))
    if config == 'OK':
      self.client_auth = True
      self.log('Config set')
    else:
      self.log('Config set failed', 40)
      exit(1)

  def connect(self):
    """
    Connects the client to RSockServer.
    Sends `"CONNECT"` to RSockServer.
    """
    if self.client_auth:
      self.log('Starting the io_copy loop')
      self.rsock_socket.sendall(bytes('CONNECT', 'utf-8'))

      connect_status = self.rsock_socket.recv(1024)
      connect_status = connect_status.decode('utf-8')
      self.log('Connected status: {}'.format(connect_status))
      if connect_status == 'OK':
        self.log('Connected to project...')
      else:
        self.log('Connect failed', 40)
        exit(1)

      # start the io_copy loop
      self.rsock_thread_running = True
      self.client_thread_running = True

      self.thread_killer_rsock = threading.Event()
      self.thread_killer_client = threading.Event()
      self.rsock_thread = threading.Thread(target=self.io_copy, name = "io_copy_server", args=("server", ))
      self.client_thread = threading.Thread(target=self.io_copy, name = "io_copy_client", args=("client", ))

      self.rsock_thread.start()
      self.client_thread.start()
    else:
      self.log('Client authentication failed', 40)
      exit(1)

  def close(self):
    """
    Closes the client, by closing sockets, then killing threads.
    """
    self.log('Closing client')
    self.rsock_socket.close()
    self.client_socket.close()
    # self.rsock_thread.join()
    # self.client_thread.join()
    self.thread_killer_rsock.set()
    self.thread_killer_client.set()
    self.log('Client closed')

  def io_copy(self, direction, stop_event):
    """
    This is the main loop that handles the data transfer between client and server.
    """
    while not stop_event.wait(1):
      self.log('Starting {} io_copy'.format(direction))

      if direction == 'client':
        client_socket = self.client_socket
        server_socket = self.rsock_socket

      elif direction == 'server':
        client_socket = self.rsock_socket
        server_socket = self.client_socket

      while self.rsock_thread_running and self.client_thread_running:
        try:
          data = client_socket.recv(1024)
          if data:
            # self.log('{} data: {}'.format(direction, data))
            server_socket.sendall(data)
          else:
            self.log('{} connection closed'.format(direction))
            break
        except Exception as e:
          self.log('Error in {} io_copy: {}'.format(direction, e), 40)
          break

      self.rsock_thread_running = False
      self.rsock_thread_running = False
      
      self.log('Stopping {} io_copy'.format(direction))


def create_connection(
  localport: int,
  user: str,
  subdomain: str,
  port: int,
  file_logger: str,
  auth: str,
  queue: Queue,
  thread_killer: threading.Event,
  notsecure: bool = False,
):
  """
  Args:
    localport: The port that the client will be listening on.
    user: The user that the client will be connecting as.
    subdomain: The subdomain that the client will be connecting to.
    port: The port that the server will be listening on.
    auth: The build auth token that the client will be using.
    queue: The queue that the client will be sending data to.
    notsecure: Whether or not to use SSL.
  """
  while not thread_killer.wait(1):
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(('localhost', localport))
    listen_socket.listen(20)

    connection_id = 0
    # print(localport, user, subdomain, port, file_logger, auth)

    while True:
      file_logger.info('Waiting for client')
      client_socket, _ = listen_socket.accept()
      file_logger.info('Client connected')

      connection_id += 1
      file_logger.info(f'Total clients connected -> {connection_id}')

      # create the client
      secure = not notsecure
      client = RSockClient(connection_id, client_socket, user, subdomain, port, file_logger, auth, secure)

      # start the client
      client.connect()

      while True:
        queue.get(block = True)
        nbx_logger.debug(f"RSock server got command to shut down")
        client.close()
  return


def port_in_use(port: int) -> bool:
  import socket
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    return s.connect_ex(('localhost', port)) == 0



def _start_connection_threads(ssh: int, *apps_to_ports: List[str], i: str, workspace_id: str):
  import sys

  if sys.platform.startswith("linux"):  # could be "linux", "linux2", "linux3", ...
    pass
  elif sys.platform == "darwin":
    pass
  elif sys.platform == "win32":
    # Windows (either 32-bit or 64-bit)
    raise Exception("Windows is unsupported platform, raise issue: https://github.com/NimbleBoxAI/nbox/issues")
  else:
    raise Exception(f"Unkwown platform '{sys.platform}', raise issue: https://github.com/NimbleBoxAI/nbox/issues")

  folder = U.join(NBOX_HOME_DIR, "tunnel_logs")
  os.makedirs(folder, exist_ok=True)
  filepath = U.join(folder, f"tunnel_{i}.log")
  file_logger = FileLogger(filepath)
  nbx_logger.info(f"Logging to {filepath}")

  # ===============

  default_ports = {
    "jupyter": 1050,
  }
  apps = {} # <localport-cloudport>
  for ap in apps_to_ports:
    app, port = ap.split(':')
    port = int(port)
    if not app or not port:
      raise ValueError(f"Invalid app:port pair {ap}")
    try:
      apps[int(app)] = port
    except:
      if app not in default_ports:
        raise ValueError(f"Unknown '{app}' should be either integer or one of {', ' .join(default_ports.keys())}")
      apps[port] = default_ports[app]
  apps[ssh] = 2222 # hard code

  ports_used = []
  for k in apps:
    if port_in_use(k):
      ports_used.append(str(k))

  if ports_used:
    raise ValueError(f"Ports {', '.join(ports_used)} are already in use")

  # check if instance is the correct one
  instance = Instance(i, workspace_id)
  if not instance.state == "RUNNING":
    # raise ValueError("Instance is not running")
    nbx_logger.error(f"Project {instance.project_id} is not running, use command:")
    nbx_logger.info(f"nbx build --i '{instance.project_id}' --workspace_id '{workspace_id}' start")
    U.log_and_exit(f"Project {instance.project_id} is not running")

  instance.start(_ssh = True)

  # create the connection
  threads = []
  queue = Queue()
  thread_killer = threading.Event()
  for localport, cloudport in apps.items():
    nbx_logger.info(f"Creating connection from {cloudport} -> {localport}")
    t = threading.Thread(target=create_connection, args=(
      localport,                       # localport
      secret.get("username"),          # user
      instance.open_data.get("url"),   # subdomain
      cloudport,                       # port
      file_logger,                     # filelogger
      instance.open_data.get("token"), # auth
      queue,                           # queue
      thread_killer,                   # thread_killer
    ))
    t.start()
    threads.append(t)

  return threads, queue, thread_killer


def _stop_connection_threads(threads: List[threading.Thread], queue: Queue, thread_killer: threading.Event):
  nbx_logger.debug(f"Stopping Rsock Server ...")
  queue.put(None)
  thread_killer.set()
  nbx_logger.debug("Waiting for Rsock Server to stop ...")
  for t in threads:
    t.join(1.0)
  return


def tunnel(ssh: int, *apps_to_ports: List[str], i: str, workspace_id: str):
  """the nbox way to SSH into your instance, by default ``"jupyter": 8888 and "mlflow": 5000``

  Usage:
    tunn.py 8000 2000:8002 -i "nbox-dev"

  Args:
    ssh: Local port to connect SSH to
    *apps_to_ports: A tuple of values ``<app_name/instance_port>:<localport>``.
      For example, ``jupyter:8888`` or ``2001:8002``
    i(str): The instance to connect to
    workspace_id (str): The workspace to connect to
  """

  threads, queue, thread_killer = _start_connection_threads(ssh, *apps_to_ports, i=i, workspace_id=workspace_id)

  try:
    # start the ssh connection on terminal
    import subprocess
    nbx_logger.info(f"Starting SSH ... for graceful exit press Ctrl+D then Ctrl+C")
    subprocess.call(f'ssh -p {ssh} ubuntu@localhost', shell=True)
  except KeyboardInterrupt:
    nbx_logger.info("KeyboardInterrupt, closing connections")
    _stop_connection_threads(threads, queue, thread_killer)

  return
