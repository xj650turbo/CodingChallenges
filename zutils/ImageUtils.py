#need to install Pillow if not already installed
#%pip install Pillow

from PIL import Image

# convert image to ascii using 0s and 1s
# usage: 
# imageFile = "ex.png" 
# asciiStr = convertImageToAscii(imageFile)
def convertImageToAscii(imageFile):
    image = Image.open(imageFile).convert('L')  # convert to gray-scale
    width, height = image.size
    asciiStr = ""
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            asciiStr += '1' if pixel <= 128 else '0'
        asciiStr += '\n'
    return asciiStr