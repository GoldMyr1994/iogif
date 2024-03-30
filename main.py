import sys
import numpy as np
import os
import uuid
import time
import util

from PIL import Image
from vector_quantization import *
from andy_warhol import andy_warhol
from gif import gif

def main(
  # source: string: image url or file path
  # source='https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/440px-Lenna_%28test_image%29.png',
  source='samples/todd.jpg',
  quantization_levels=16,
  gif_duration=4,
  gif_frames_per_second=10,
  andy_warhol_intermediate_resize=512,
  andy_warhol_module_size=128,
  andy_warhol_module_per_side=4,
  ):
  img = util.read_image(source)
  img = np.array(img)

  quantized, _, _ = LBG(img, quantization_levels)
  quantized = Image.fromarray(quantized)

  _id = uuid.uuid4()
  foldername = os.path.join('out',f'{_id}')
  quantized_filename = os.path.join(f'{foldername}',f'LBG-{quantization_levels}.png')

  os.makedirs(foldername)
  quantized.save(quantized_filename)

  for i in range(gif_duration*gif_frames_per_second - 1):
    util.random_colormap(quantized).save(f'{foldername}/{uuid.uuid4()}.png')

  filenames = util.get_images_filenames_from_folder(foldername)

  gif(filenames, f'{foldername}/gif.gif', gif_duration)

  missing = andy_warhol_module_per_side**2 - (gif_duration*gif_frames_per_second - 1)
  if missing > 0:
    for i in range(int(missing)):
      util.random_colormap(quantized).save(f'{foldername}/{uuid.uuid4()}.png')

  filenames = util.get_images_filenames_from_folder(foldername)

  andy_warhol_image = andy_warhol(filenames, andy_warhol_intermediate_resize, andy_warhol_module_size, andy_warhol_module_per_side)
  andy_warhol_image.save(f'{foldername}/andy_warhol.png')

if __name__ == "__main__":
  main()

