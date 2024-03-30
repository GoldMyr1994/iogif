from PIL import Image
import numpy as np
import os

imageObject = Image.open("./io.gif", mode="r")

for frame in range(0,imageObject.n_frames):
  imageObject.seek(frame)
  image = np.asarray(imageObject.convert("RGB"))[100:640, 500:1040]
  if (not os.path.isdir('tmp')):
      os.mkdir('tmp')
  Image.fromarray(image).imwrite(f"tmp/image{frame}.png")
