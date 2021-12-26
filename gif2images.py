# Reading an animated GIF file using Python Image Processing Library - Pillow
from PIL import Image
from PIL import GifImagePlugin
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

imageObject = Image.open("./io.gif", mode="r")

for frame in range(0,imageObject.n_frames):
  imageObject.seek(frame)
  img = np.asarray(imageObject.convert("RGB"))[100:640, 500:1040]
  if (not os.path.isdir('tmp')):
      os.mkdir('tmp')
  cv2.imwrite(f"tmp/img{frame}.png", img)
