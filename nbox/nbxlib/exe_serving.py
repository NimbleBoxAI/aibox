# https://github.com/apache/airflow/issues/7870

import inspect
from typing import Any, Dict

try:
  from pydantic import create_model
except ImportError:
  # if this is happening to you sir, why don't you come work with us?
  pass

from nbox.operator import Operator, OperatorType
from nbox.utils import py_from_bs64, py_to_bs64

def get_fastapi_routes(op: Operator):
  """To keep seperation of responsibility the paths are scoped out like all the functions are
  in the /method_{...} and all the custom python code is in /nbx_py_rpc"""
  if op._op_type == OperatorType.WRAP_CLS:
    routes = []
    # add functions that the user has exposed
    wrap_class = op._op_wrap
    for p in dir(wrap_class.__class__):
      if p.startswith("__"):
        continue
      fn = getattr(wrap_class, p)
      routes.append((f"/method_{p}", get_fastapi_fn(fn)))

    # add functions that the python itself can support
    routes.append((f"/nbx_py_rpc", nbx_py_rpc(op)))
  else:
    routes = [("/forward", get_fastapi_fn(op.forward)),]
  return routes


# builder method is used to progrmatically generate api routes related information for the fastapi app
def get_fastapi_fn(fn):
  from pydantic import create_model
  
  # we use inspect signature instead of writing our own ast thing
  signature = inspect.signature(fn)
  data_dict = {}
  for param in signature.parameters.values():
    default = param.default
    annot = param.annotation
    if default == inspect._empty:
      default = None
    if param.annotation == inspect._empty:
      annot = Any
    data_dict[param.name] = (annot, default)

  # if your function takes in inputs then it is expected to be sent as query params, so create a pydantic
  # model and FastAPI will take care of the rest
  name = f"{fn.__name__}_Request"
  base_model = create_model(name, **data_dict)

  # pretty simple forward function, note that it gets operator using get_op which will be a cache hit
  async def generic_fwd(req: base_model):
    # need to add serialisation to this function because user won't by default send in a serialised object
    data = req.dict()
    try:
      out = fn(**data)
      return {"success": True, "value": py_to_bs64(out)}
    except Exception as e:
      return {"success": False, "message": str(e)}

  return generic_fwd


def nbx_py_rpc(op: Operator):
  base_model = create_model("nbx_py_rpc", rpc_name = (str, ""), key = (str, ""), value = (str, ""),)
  _nbx_py_rpc = NbxPyRpc(op)
  
  async def forward(req: base_model):
    # no need to add serialisation because the NbPyRpc class will handle it
    data = req.dict()
    return _nbx_py_rpc(data)

  return forward


class NbxPyRpc(Operator):
  """This object is a shallow class that is used as a router of functions. Distributed computing combined with
  user friendliness of python means that some methods acn be routed and managed as long as there is a wire
  protocol. So here it is:

  request = {
    "rpc_name": "__getattr__",
    "key": "string",            # always there
    "value": "b64-cloudpickle", # optional for functions
  }

  response = {
    "success": bool,
    "message": str,   # optional, will be error in case of failure
    "value": str,     # optional, will be b64-cloudpickle or might be empty ex. del
  }

  we should also add some routes to support a subset of important language features:

  1. __getattr__: obtain any value by doing: `obj.x`
  2. __getitem__: obtain any value by doing: `obj[x]`
  3. __setitem__: set any value by doing: `obj[x] = y`
  4. __delitem__: delete any value by doing: `del obj[x]`
  6. __iter__: iterate over any iterable by doing: `for x in obj`
  7. __next__: get next value from an iterator by doing: `next(obj)`
  8. __len__: get length of any object by doing: `len(obj)`
  9. __contains__: check if an object contains a value by doing: `x in obj`

  The reason we have chosen these for starting is that they can be used to represent any
  data structure required and get/set information from it. We can add more later like
  __enter__ and __exit__ to support context managers. Others like numerical operations
  __add__ and __sub__ doesn't really make sense. Maybe one day when we have neural networks
  but even then it's not clear how we would use them.
  """
  def __init__(self, op: Operator):
    super().__init__()
    self.wrapped_cls = op

  def forward(self, data) -> Dict[str, str]:
    _k = set(tuple(data.keys())) - set(["rpc_name", "key", "value"])
    if _k:
      return {"success": False, "message": f"400: invalid keys: {_k}"}
    rpc_name = data.get("rpc_name", "")
    if rpc_name not in {
      "__getattr__",
      "__getitem__",
      "__setitem__",
      "__delitem__",
      "__iter__",
      "__next__",
      "__len__",
      "__contains__",
    }:
      return {"success": False, "message": f"400: invalid rpc_name: {rpc_name}"}

    key = data.get("key", "")
    value = data.get("value", "")

    if key:
      key = py_from_bs64(key)
    if value:
      value = py_from_bs64(value)

    fn = {
      "__getattr__": (self.fn_getattr, key),
      "__getitem__": (self.fn_getitem, key),
      "__setitem__": (self.fn_setitem, key, value),
      "__delitem__": (self.fn_delitem, key),
      "__iter__": (self.fn_iter),
      "__next__": (self.fn_next),
      "__len__": (self.fn_len),
      "__contains__": (self.fn_contains, key),
    }

    fn, *args = fn[rpc_name]
    
    try:
      out = fn(*args)
      return out
    except Exception as e:
      return {"success": False, "message": str(e)}
  
  def fn_getattr(self, key):
    out = getattr(self.wrapped_cls._op_wrap, key)
    return {"success": True, "value": py_to_bs64(out)}

  def fn_getitem(self, key):
    out = self.wrapped_cls._op_wrap[key]
    return {"success": True, "value": py_to_bs64(out)}
  
  def fn_setitem(self, key, value):
    self.wrapped_cls._op_wrap[key] = value
    return {"success": True}

  def fn_delitem(self, key):
    del self.wrapped_cls._op_wrap[key]
    return {"success": True}

  def fn_iter(self):
    out = iter(self.wrapped_cls._op_wrap)
    return {"success": True, "value": py_to_bs64(out)}

  def fn_next(self):
    out = next(self.wrapped_cls._op_wrap)
    return {"success": True, "value": py_to_bs64(out)}

  def fn_len(self):
    out = len(self.wrapped_cls._op_wrap)
    return {"success": True, "value": py_to_bs64(out)}

  def fn_contains(self, key):
    out = key in self.wrapped_cls._op_wrap
    return {"success": True, "value": py_to_bs64(out)}
