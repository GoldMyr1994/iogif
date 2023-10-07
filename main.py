import sys
sys.path.append('/Users/mauroconte/Desktop/iogif/src/')

import numpy as np
import cv2
import os
import uuid
import time

import util
from vector_quantization import *

def main(
  # source: string: image url or file path
  source='https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/440px-Lenna_%28test_image%29.png',
  quantization_levels=4,
  png_duration=4,
  png_frames_per_second=10,
  andy_warhol_module_size=128,
  andy_warhol_module_number=4,
  ):
  img = util.read_image(source, 2**9)
  if img is None:
    exit("Image not found")

  img = np.array(img)

  q, _, _ = LGB(img, quantization_levels)

  _id = uuid.uuid4()

  os.makedirs(f'out/{_id}')
  cv2.imwrite(f'out/{_id}/LGB-{quantization_levels}.png',q)
  img = cv2.imread(f'out/{_id}/LGB-{quantization_levels}.png')

  for i in range(png_duration*png_frames_per_second - 1):
    img = util.colormap(img,[])
    cv2.imwrite(f'out/{_id}/{uuid.uuid4()}.png', img)

  util.make_gif_from_folder(f'out/{_id}', 'gif.gif', png_duration)
  andy_warhol_image = util.make_andy_warhol(f'out/{_id}', andy_warhol_module_size, andy_warhol_module_number)
  cv2.imwrite("andy_warhol.png", andy_warhol_image)

if __name__ == "__main__":
  main()

