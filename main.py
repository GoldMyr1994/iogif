import sys
sys.path.append('/Users/mauroconte/Desktop/iogif/src/')

import numpy as np
import cv2
import os
import uuid
import time

import util
from vector_quantization import *

def main():

  _id = uuid.uuid4()

  # 'src/io.png'
  # 'src/luna.jpeg'
  # 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/440px-Lenna_%28test_image%29.png'
  # 'https://media.gqitalia.it/photos/6089331d8a8620fb02fad5ba/1:1/w_960,c_limit/Billie%20Eilish_cover%20album%20Happier%20Than%20Ever.jpg'

  img = util.read_image('src/luna.jpeg')

  if img is None:
    exit("Image not found")
  img = np.array(img)

  print("Vector Quantization (LBG) on iamge of shape:", img.shape)
  q, _, _ = LGB(img, 4)
  cv2.imwrite("out/q4.png",q)

  img = cv2.imread('out/q4.png')
  os.makedirs(f'out/{_id}')
  for i in range(10):
    print("colormap", i)
    img = util.colormap(img,[])
    cv2.imwrite(f'out/{_id}/{uuid.uuid4()}.png', img)

  util.make_gif_from_folder(f'out/{_id}')

  # make something with the generated images

if __name__ == "__main__":
  main()

