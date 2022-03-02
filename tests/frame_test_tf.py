from nbox import load, Model
from nbox.utils import get_image
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
import tensorflow as tf
from tensorflow import keras
from keras import layers
from tensorflow.keras.applications.resnet50 import decode_predictions
from keras.models import Sequential
from keras import Input
from keras.layers import Dense
import numpy as np

def br():
  print("*"*50, "\n")

def fn(x):
    import tensorflow as tf
    if not isinstance(x, tf.Tensor):
        x = tf.convert_to_tensor(x, dtype=tf.float32)
    return x*2

def test_resnet():
  resnet_model = tf.keras.applications.ResNet50(
      include_top=True,
      weights="imagenet",
      classes=1000,
  )
  x = tf.random.uniform([1, 224, 224, 3])

  res = Model(resnet_model, None)
  res.eval()
  first_out = res(x).outputs

  new_res = Model.deserialise(
    res.serialise(
      input_object = x,
      model_name = "test69",
      export_type = "SaveModel",
      _unit_test = True
    )
  )

  # now pass data through the new model
  second_out = new_res(x).outputs
  assert np.all(first_out == second_out)
  return decode_predictions(second_out.numpy(), top = 5)

def feed_forward():
  model = Sequential(name="Model-with-One-Input")
  model.add(Input(shape=(1,), name='Input-Layer'))
  model.add(Dense(2, activation='softplus', name='Hidden-Layer'))
  model.add(Dense(1, activation='sigmoid', name='Output-Layer'))

  x = np.random.uniform(size=(224))

  model = Model(model, None)
  model.eval()
  first_out = model(x).outputs
  m2 = Model.deserialise(
    model.serialise(
      input_object = x,
      model_name = "test69",
      export_type = "h5",
      _unit_test = True
    )
  )
  second_out = m2(x).outputs
  assert np.all(second_out == first_out)
  return second_out.shape


def test_tiny_gpt_SaveModel():
  def gen(model, tokenizer, text):
    pred = []
    for i in range(10):
      encoded_input = tokenizer(text, return_tensors='tf')
      logits = model(encoded_input).outputs.logits
      logits = tf.math.softmax(logits[:,-1,:], axis = 1)
      p = str(tokenizer.decode(tf.math.argmax(logits, axis=1)))
      text = text.join(" "+p)
      if len(text) > 512:
        text = text[-256:]
      pred.append(p)
    return "".join(pred)

  def fn(x):
    dict = {}
    for i in x.keys():
      dict[i] = x[i]
    return dict

  from transformers import AutoTokenizer
  tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
  model = TFGPT2LMHeadModel.from_pretrained("sshleifer/tiny-gpt2")
  text = "Let us generate some text for nbox."
  model = Model(model, fn)
  model.eval()

  first_out = gen(model, tokenizer, text)

  m2 = Model.deserialise(
    model.serialise(
      input_object = tokenizer(text, return_tensors='tf'),
      model_name = "test69",
      export_type = "SaveModel",
      _unit_test = True
    )
  )
  second_out = gen(m2, tokenizer, text)
  assert np.all(second_out == first_out)
  return second_out


def test_tiny_gpt_ONNX():
  import tensorflow as tf

  def fn(x):
    print("x tensor",x)
    return {"x":x}

  model = tf.keras.applications.ResNet50(
     include_top=True,
     weights="imagenet",
     classes=1000,
  )

  x = tf.random.uniform([1, 224, 224, 3])
  res = Model(model, fn)
  res.eval()
  first_out = res(x).outputs

  print(decode_predictions(first_out.numpy(), top = 5),  "\n\n")
  new_res = Model.deserialise(
  res.serialise(
     input_object = x,
     model_name = "test69",
      export_type = "onnx",
      _unit_test = True
    )
  )
  second_out =  new_res(x).outputs[0][0]
  comparison = first_out.numpy() == second_out
  print("first_out", first_out.numpy())
  print("second out", second_out)
  assert comparison.all() == True
  return second_out




br()
#Test FeedForward
# print("Output for Feed Forward Network:- \n", feed_forward())
# br()

# print("Output for tiny GPT-2 through SaveModel: \n", test_tiny_gpt_SaveModel())
# br()

print("Output for tiny GPT-2 through ONNX : \n", test_tiny_gpt_ONNX())
br()

# #Test Resnet
# br()
# print("Output for Resnet50 : \n", test_resnet())
