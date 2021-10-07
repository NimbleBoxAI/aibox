import nbox
from nbox.utils import get_image

# load pretrained model
model = nbox.load(
    "torchvision/resnet18",
    pretrained=True,
)

# literally pass model a URL and it will process it
image_url = "https://github.com/NimbleBoxAI/nbox/raw/master/tests/assets/cat.jpg"
out = model(image_url)
print(out[0].topk(5))

image = get_image(image_url)  # get the PIL.Image object
image = image.resize((244, 244))  # you can skip the following shape if the shape is already correct

url, key = model.deploy(
    input_object=image,  # simply provide the input_object and watch the Terminal
    wait_till_deployment=True,  # this will return the url endpoint and key
)

print("url:", url)
print("key:", key)

# load the model and use it without any difference in API
model = nbox.load(url, key)
out = model(image_url)
print(out[0].topk(5))
