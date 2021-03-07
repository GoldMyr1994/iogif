import requests
from PIL import Image
import os
import shutil
import uuid
import imageio
import numpy as np
import cv2
import time

COLORS =  [np.random.randint(0,256,size=3) for i in range(int(1e4))]
C_INDEX = 1

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
  print(len(images))
  make_gif(images)


def clean_temp():
  for root, dirs, files in os.walk("out/temp/"):
    for f in files:
        if f == '.gitkeep':
          continue
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

def rescale_image(image, width):
  h = width*(image.shape[0]/image.shape[1])
  return cv2.resize(image, (width, int(h)))
  
def read_image_from_url(image_url, max_width=800):
  tmp_path = f"out/temp/temp_imge_{uuid.uuid4()}.png"
  # Exception Handling for invalid requests
  try:
    # Creating an request object to store the response
    ImgRequest = requests.get(image_url)

    # Verifying whether the specified URL exist or not
    if ImgRequest.status_code == requests.codes.ok:

      # Opening a file to write bytes from response content
      # Storing this onject as an image file on the hard drive
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
    img = np.asarray(img)
    if img.shape[1] > max_width: 
      return rescale_image(np.asarray(img), max_width)
    else:
      return np.asarray(img)

def colormap(img, colors, tol=1e-3):
  pixels = img.reshape(img.shape[0] * img.shape[1], 3)
  unique_pixels = np.unique(pixels, axis=0)
  colors.extend([ np.random.randint(0,256,size=3) for i in range(len(unique_pixels)-len(colors))])
  colors = colors[:len(unique_pixels)]
  out = img.copy().astype(np.uint8)
  for index, el in enumerate(unique_pixels):
    out[np.where(np.linalg.norm(img - el,axis=-1)<1e-3)] = colors[index]
  return out
