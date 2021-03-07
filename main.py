import numpy as np
import cv2
import os
import uuid
import time

import util
from vector_quantization import *

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

def main():

  _id = uuid.uuid4()
  
  img = util.read_image_from_url('URL_TO_IMAGE')
  
  print("Vector Quantization (LBG) on iamge of shape:", img.shape)
  q, _, _ = LGB(img, 4)
  cv2.imwrite("out/q4.png",q)

  img = cv2.imread('out/q4.png')
  os.makedirs(f'out/{_id}')
  for i in range(100):
    print("colormap", i)
    img = util.colormap(img,[])
    cv2.imwrite(f'out/{_id}/{uuid.uuid4()}.png', img)

  util.make_gif_from_folder("out/d92f76b1-e5d4-4259-bd3a-95eaa785257b")

if __name__ == "__main__":
  main()

  