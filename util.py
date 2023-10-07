import sys
sys.path.append('/Users/mauroconte/Desktop/iogif/')

import requests
from PIL import Image, ImageFile, ImageOps
import os
import shutil
import uuid
import imageio
import numpy as np
import time
from urllib.parse import urlparse

ImageFile.LOAD_TRUNCATED_IMAGES = True

def is_url(url):
    return

def ensure_square_image(image, length):
  w, h = image.size[:2]
  w2, h2 = w//2, h//2
  if h>w:
    image = image.crop((0,h2-w2,w,h2+w2))
  elif h<w:
    image = image.crop((w2-h2,0,w2+h2,h))
  image = image.resize((length, length))
  return image


def make_gif(images, duration=0.04):
  imageio.mimsave(os.path.join('out/movie.gif'), images) # modify duration as needed

def make_gif_from_folder(folder):
  #image_folder = os.fsencode(folder)
  filenames = []
  for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.jpg','.jpeg', '.png', '.gif') ):
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

def read_image(source_string, length=800):
  if urlparse(source_string).scheme != "":
    return read_image_from_url(source_string, length)
  return read_image_from_disk(source_string, length)

def read_image_from_disk(image_path, length=800):
  try:
    original_image = Image.open(image_path)
    img = ImageOps.exif_transpose(original_image)
    return ensure_square_image(img, length)
  except Exception as e:
    print(str(e))
    return None

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
      return None
  except Exception as e:
    print(str(e))
    return None
  img = Image.open(tmp_path)
  return ensure_square_image(img, length)

def colormap(img, colors, tol=1e-3):
  pixels = img.reshape(img.shape[0] * img.shape[1], 3)
  unique_pixels = np.unique(pixels, axis=0)
  colors.extend([ np.random.randint(0,256,size=3) for i in range(len(unique_pixels)-len(colors))])
  colors = colors[:len(unique_pixels)]
  out = img.copy().astype(np.uint8)
  for index, el in enumerate(unique_pixels):
    out[np.where(np.linalg.norm(img - el,axis=-1)<1e-3)] = colors[index]
  return out

def compose_h_w(module=64, n=9):
  images = list(map(lambda name: cv2.imread(f'tmp/{name}',1), os.listdir('tmp')))
  randoms = []
  if n**2-len(images)>0:
    randoms = np.random.randint(0, len(images), n**2-len(images))

  for index in randoms:
    images.append(images[index])

  for i in range(len(images)):
    images[i] = cv2.resize(images[i], (module, module), interpolation = cv2.INTER_AREA)

  base = np.zeros((module*n,module*n, 3),np.uint8)
  for i in range(n**2):
    r,c = i//n, i%n
    base[r*module:(r+1)*module, c*module:(c+1)*module] = images[i]

  cv2.imwrite("io9x9.png",base)
