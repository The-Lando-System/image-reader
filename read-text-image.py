import argparse
from PIL import Image


parser = argparse.ArgumentParser(description='Provide a path to an image containing text')
parser.add_argument('image', help='Path to the image file')
args = parser.parse_args()


print("Hello World! Here is my file: " + args.image)

# im = Image.open("./training-data/calibri-alphabet.png")
im = Image.open(args.image)

print(im.format, im.size, im.mode)

pixels = list(im.getdata())

print(str(len(pixels)))


