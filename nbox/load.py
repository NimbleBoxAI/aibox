# singluar loader file for all models in nbox

import re
import json
import inspect
from typing import Dict

from .model import Model
from .utils import fetch, isthere, logger

model_key_regex = re.compile(r"^(\w+)(\/[\w\/-]+)?(:*[\w+:]+)?$")

# util functions
def remove_kwargs(model_fn, kwargs):
  """take in the ``model_fn`` and only keep variables from kwargs that can be consumed"""
  # compare variables between the model_fn and kwargs if they are different then remove it with warning
  arg_spec = inspect.getfullargspec(model_fn)
  if kwargs and arg_spec.varkw != None:
    diff = set(kwargs.keys()) - set(arg_spec.args)
    for d in list(diff):
      kwargs.pop(d)
  return kwargs


# --- model loader functions: add your things here
# guide: all models are indexed as follows
# {
#  "key": (builder_function, "category")
#
#  # to be moved to
#  "key": (builder_function, "task_type", "source", "pre", "task", "post")
# }
#
# Structure of each loader function looks as follows:
# def loader_fn() -> <dict as above>
#
# Each model builder function looks as follows:
# def model_builder() -> (model, model_kwargs)

@isthere("efficientnet_pytorch", soft = False)
def _efficientnet_pytorch_models(pretrained=False, **kwargs):
  import efficientnet_pytorch

  if pretrained:
    model_fn = efficientnet_pytorch.EfficientNet.from_pretrained
  else:
    model_fn = efficientnet_pytorch.EfficientNet.from_name

  kwargs = remove_kwargs(model_fn, kwargs)
  return model_fn(**kwargs)


@isthere("torchvision", soft = False)
def _torchvision_models(model, pretrained=False, **kwargs) -> Dict:
  # tv_mr = torchvision models registry
  # this is a json object that maps all the models to their respective methods from torchvision
  # the trick to loading is to eval the method string
  tv_mr = json.loads(fetch("https://raw.githubusercontent.com/NimbleBoxAI/nbox/master/assets/pt_models.json").decode("utf-8"))
  model_fn = tv_mr.get(model, None)
  if model_fn == None:
    raise IndexError(f"Model: {model} not found in torchvision")

  # torchvision is imported here, if it is imported in the outer method, eval fails
  # reason: unknown
  import torchvision

  model_fn = eval(model_fn)
  kwargs = remove_kwargs(model_fn, kwargs)
  model = model_fn(pretrained=pretrained, **kwargs)
  return model


@isthere("transformers", soft = False)
def _transformers_models(model, model_instr, **kwargs):
  import transformers

  _auto_loaders = {x: getattr(transformers, x) for x in dir(transformers) if x[:4] == "Auto" and x != "AutoConfig"}

  model_instr = model_instr.split("::")
  if len(model_instr) == 1:
    auto_model_type = model_instr[0]
  else:
    # if the task is given, validate that as well
    auto_model_type, task = model_instr
    assert task in [
      "generation",
      "masked_lm",
    ], "For now only the following are supported: `generation`, `masked_lm`"

  # initliase the model and tokenizer object
  tokenizer = transformers.AutoTokenizer.from_pretrained(model, **kwargs)

  # All the tokenizers must contain the pad_token, by default we set it to eos_token
  if not tokenizer.pad_token:
    tokenizer.add_special_tokens({"pad_token": tokenizer.eos_token})

  # tokenizer.pad_token = tokenizer.eos_token if not tokenizer.pad_token_id else tokenizer.pad_token
  model = _auto_loaders[auto_model_type].from_pretrained(model, **kwargs)

  # return the model and tokenizer
  return model, {"tokenizer": tokenizer}


### ----- pretrained models master index
# add code based on conditionals, best way is to only include those that
# have proper model building code like transformers, torchvision, etc.

PRETRAINED_MODELS = {
  "efficientnet_pytorch": _efficientnet_pytorch_models,
  "torchvision": _torchvision_models,
  "transformers": _transformers_models,
}


# ---- load function has to manage everything and return Model object properly initialised


def load(model, pre_fn = None, verbose=False, **loader_kwargs) -> Model:
  """This function loads the nbox.Model object from the pretrained models index.

  Args:

    registry (str): key for which to load the model, the structure looks as follows:

      .. code-block:: python

        "source/(source/key)::<pre::task::post>"


    nbx_api_key (str, optional): If model_key_or_url has type `url` then pass the key corresponding url
    verbose (bool, optional): If True, prints logs
    cloud_infer (bool, optional): If true uses Nimblebox deployed inference and logs in
      using `nbx_api_key`. Defaults to False.
    loader_kwargs (dict, optional): keyword arguments to be passed to the loader function.

  Raises:
    ValueError: If `source` is not found
    IndexError: If `source` is found but `source/key` is not found

  Returns:
    nbox.Model
  """
  # the input key can also contain instructions on how to run a particular models and so
  model_key_parts = re.findall(model_key_regex, model)
  if not model_key_parts:
    raise ValueError(f"Key: {model} incorrect, please check!")

  # this key is valid, now get it's components
  src, src_key, model_instr = model_key_parts[0]
  src_key = src_key.strip("/") # remove leading and trailing slashes
  model_instr = model_instr.replace(":", "") # remove the :

  model_fn = PRETRAINED_MODELS.get(src, None)
  if model_fn is None:
    raise IndexError(f"Model: {src} not found")

  # now just load the underlying graph and the model and off you go
  model = model_fn(model=src_key, model_instr=model_instr, **loader_kwargs)
  out = Model(
    m0 = model,
    m1 = pre_fn,
    verbose=verbose,
  )
  return out
