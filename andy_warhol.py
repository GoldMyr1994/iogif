from PIL import Image
import util
import numpy as np

def andy_warhol(filenames, intermediate_resize=512, module_size=64, module_per_side=9):
  images = list(map(lambda filename: util.ensure_square_image(Image.open(filename),intermediate_resize), filenames))
  base = np.zeros((module_size*module_per_side,module_size*module_per_side, 3),dtype=np.uint8)
  for i in range(module_per_side**2):
    r,c = i//module_per_side, i%module_per_side
    resized = images[i].resize((module_size, module_size))
    base[r*module_size:(r+1)*module_size, c*module_size:(c+1)*module_size] = np.array(resized, dtype=np.uint8)
  return Image.fromarray(base)
