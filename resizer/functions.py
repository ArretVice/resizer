from PIL import Image


# Image.resize((width, height)) - returns resized copy
def resize_image(image, width, height):
    return Image.open(image).resize((width, height))
