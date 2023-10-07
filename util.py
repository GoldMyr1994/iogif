import sys
sys.path.append('/Users/mauroconte/Desktop/iogif/')

import requests
from PIL import Image
import os
import shutil
import uuid
import imageio
import numpy as np
import cv2
import time
import util

COLORS =  [np.random.randint(0,256,size=3) for i in range(int(1e4))]
C_INDEX = 1

def rescale_image(image, width):
  h = width*(image.shape[0]/image.shape[1])
  return cv2.resize(image, (width, int(h)))

def ensure_square_image(image, length):
  print(image.shape)
  w,h = image.shape[:2]
  if w > h:
    image = image[(w-h)//2:(w-h)//2+h,:]
  elif h > w:
    image = image[:,(h-w)//2:(h-w)//2+w]
  return rescale_image(image, length)


def make_gif(images):
  imageio.mimsave(os.path.join('out/movie.gif'), images, duration = 0.04) # modify duration as needed

def make_gif_from_folder(folder):
  #image_folder = os.fsencode(folder)
  filenames = []
  for file in os.listdir(folder):

    filename = os.fsdecode(file)
    if filename.endswith( ('.jpeg', '.png', '.gif') ):
      filenames.append(f"{folder}/{filename}")

  filenames.sort()
  images = list(map(lambda filename: imageio.imread(filename), filenames))
  make_gif(images)


def clean_temp():
  for root, dirs, files in os.walk("out/temp/"):
    for f in files:
      if f == '.gitkeep':
        continue
      os.unlink(os.path.join(root, f))
    for d in dirs:
      shutil.rmtree(os.path.join(root, d))

def read_image_from_disk(image_path, max_width=800):
  img = Image.open(image_path)
  return ensure_square_image(np.asarray(img), max_width)

def read_image_from_url(image_url, length=800):
  tmp_path = f"out/temp/temp_imge_{uuid.uuid4()}.png"
  try:
    ImgRequest = requests.get(image_url)
    if ImgRequest.status_code == requests.codes.ok:
      img = open(tmp_path,"wb")
      img.write(ImgRequest.content)
      img.close()
    else:
      print(ImgRequest.status_code)

  except Exception as e:
    print(str(e))
  finally:
    img = Image.open(tmp_path)
    clean_temp()
    return ensure_square_image(np.asarray(img), length)

def colormap(img, colors, tol=1e-3):
  pixels = img.reshape(img.shape[0] * img.shape[1], 3)
  unique_pixels = np.unique(pixels, axis=0)
  colors.extend([ np.random.randint(0,256,size=3) for i in range(len(unique_pixels)-len(colors))])
  colors = colors[:len(unique_pixels)]
  out = img.copy().astype(np.uint8)
  for index, el in enumerate(unique_pixels):
    out[np.where(np.linalg.norm(img - el,axis=-1)<1e-3)] = colors[index]
  return out

def get_io():
  return util.read_image_from_disk('src/io.png')

def get_luna():
  return util.read_image_from_disk('src/luna.jpeg')

def get_lena():
  return util.read_image_from_url('https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/440px-Lenna_%28test_image%29.png')

def get_billie():
  return util.read_image_from_url('https://media.gqitalia.it/photos/6089331d8a8620fb02fad5ba/1:1/w_960,c_limit/Billie%20Eilish_cover%20album%20Happier%20Than%20Ever.jpg')
