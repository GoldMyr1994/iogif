import sys
import requests
import os
import shutil
import uuid
import numpy as np
import time
import tempfile

from PIL import Image, ImageFile, ImageOps
from urllib.parse import urlparse

ImageFile.LOAD_TRUNCATED_IMAGES = True

def ensure_square_image(image, length):
  w, h = image.size[:2]
  w2, h2 = w//2, h//2
  if h>w:
    image = image.crop((0,h2-w2,w,h2+w2))
  elif h<w:
    image = image.crop((w2-h2,0,w2+h2,h))
  image = image.resize((length, length))
  return image

def get_images_filenames_from_folder(folder):
  filenames = []
  for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.jpg','.jpeg', '.png', '.gif') ):
      filenames.append(f"{folder}/{filename}")
  return filenames

def read_image(source_string):
  if urlparse(source_string).scheme != "":
    return read_image_from_url(source_string)
  return read_image_from_disk(source_string)

def read_image_from_disk(image_path):
  try:
    original_image = Image.open(image_path)
    image = ImageOps.exif_transpose(original_image)
    return image
  except Exception as e:
    exit(e)

def read_image_from_url(image_url):
  tmp = tempfile.NamedTemporaryFile()
  try:
    ImageRequest = requests.get(image_url)
    if ImageRequest.status_code == requests.codes.ok:
      tmp.write(ImageRequest.content)
    else:
      exit('ImageRequest ERROR',ImageRequest.status_code )
  except Exception as e:
    tmp.close()
    exit(e)
  image = Image.open(tmp.name)
  tmp.close()
  return image

COLORS = [ np.random.randint(0,256,size=3) for i in range(1000000) ]

def random_colormap(image, tol=1e-3):
  global COLORS
  img = np.asarray(image)
  pixels = img.reshape(img.shape[0] * img.shape[1], 3)
  unique_pixels = np.unique(pixels, axis=0)

  colors = []
  for i in range(len(unique_pixels)):
    colors.append(COLORS[0])
    del COLORS[0]

  out = img.copy().astype(np.uint8)
  for index, el in enumerate(unique_pixels):
    out[np.where(np.linalg.norm(img - el,axis=-1)<1e-3)] = colors[index]
  return Image.fromarray(out)


