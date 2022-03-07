"""
Jobs
====

``nbox.Job`` is a wrapper to the APIs that's it.
"""

import sys

from nbox.hyperloop.job_pb2 import NBXAuthInfo

from ..utils import logger
from ..init import nbox_grpc_stub
from ..network import Cron

class Job:
  def __init__(self, id, workspace_id =None):
    self.id = id
    self.workspace_id = workspace_id
    self.auth_info = NBXAuthInfo(workspace_id=self.workspace_id)
    self.update()

  def change_schedule(self, new_schedule: Cron):
    # nbox should only request and server should check if possible or not
    pass

  def stream_logs(self, f = sys.stdout):
    # this function will stream the logs of the job in anything that can be written to
    import grpc
    from ..hyperloop.nbox_ws_pb2 import JobLogsRequest
    
    logger.info(f"Streaming logs of job {self.id}")
    try:
      log_iter = nbox_grpc_stub.GetJobLogs(JobLogsRequest(job = self._this_job))
    except grpc.RpcError as e:
      logger.error(f"Could not get logs of job {self.id}")
      raise e

    for job_log in log_iter:
      for log in job_log.log:
        f.write(log)
        f.flush()

  def delete(self):
    import grpc
    from ..hyperloop.nbox_ws_pb2 import JobInfo
    try:
      nbox_grpc_stub.DeleteJob(JobInfo(job = self._this_job,))
    except grpc.RpcError as e:
      logger.error(f"Could not delete job {self.id}")
      raise e

  def update(self):
    import grpc
    from ..hyperloop.nbox_ws_pb2 import JobInfo
    from ..hyperloop.job_pb2 import Job as JobProto, NBXAuthInfo
    logger.info("Updating job info")

    try:
      job: JobProto = nbox_grpc_stub.GetJob(JobInfo(job = JobProto(id = self.id, auth_info=self.auth_info)))
    except grpc.RpcError as e:
      logger.error(f"Could not get job {id}")
      raise e
    for descriptor, value in job.ListFields():
      setattr(self, descriptor.name, value)
    self._this_job = job
    self._this_job.auth_info.CopyFrom(self.auth_info)

  def trigger(self):
    import grpc
    from nbox.hyperloop.nbox_ws_pb2 import JobInfo
    logger.info(f"Triggering job {self.id}")
    
    try:
      
      nbox_grpc_stub.TriggerJob(JobInfo(job=self._this_job))
    except grpc.RpcError as e:
      logger.error(f"Could not trigger job {self.id}")
      raise e

