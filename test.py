# Imports PIL module
from PIL import Image

# creating a image object (new image object) with
# RGB mode and size 200x200
im =Image.new(mode="RGB", size=(800, 600))

# This method will show image in any image viewer
im.save('light.png')
# a = [400]*5*3
# x, y = 4, 2
# a[5*y + x] = 600
# print(a)