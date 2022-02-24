r"""This submodule concerns itself with conversion of different framworks to other frameworks.
It achieves this by providing a fix set of functions for each framework. There are a couple of
caveats that the developer must know about.

1. We use joblib to serialize the model, see `reason <https://stackoverflow.com/questions/12615525/what-are-the-different-use-cases-of-joblib-versus-pickle>`_ \
so when you will try to unpickle the model ``pickle`` will not work correctly and will throw the error
``_pickle.UnpicklingError: invalid load key, '\x00'``. So ensure that you use ``joblib``.

2. Serializing torch models directly is a bit tricky and weird, you can read more about it
`here <https://github.com/pytorch/pytorch/blob/master/torch/csrc/jit/docs/serialization.md>`_,
so technically pytorch torch.save() automatically pickles the object along with the required
datapoint (model hierarchy, constants, data, etc.)

Lazy Loading
------------

All the dependencies are checked at runtime only, meaning all the modules coded can be referenced
removing blockers and custom duct taping.

Documentation
-------------
"""

from .on_ml import  *
from .on_operators import *

ALL_PROTOCOLS = [NBXModel, TensorflowModel, TorchModel, SklearnModel, ONNXRtModel]

def register_new_on_ml_protocol(proto: FrameworkAgnosticProtocol):
  ALL_PROTOCOLS.append(proto)


def get_model_mixin(i0, i1 = None, deserialise = False):
  all_e = []
  for m in ALL_PROTOCOLS:
    try:
      # if this is the correct method 
      if not deserialise:
        return m(i0, i1)
      else:
        return m.deserialise(i0)
    except InvalidProtocolError as e:
      all_e.append(f"--> ERROR: {m.__class__.__name__}: {e}")

  raise InvalidProtocolError(
    f"Unkown inputs [{deserialise}]: {type(i0)} {type(i1)}!" + \
    "\n".join(all_e)
  )
