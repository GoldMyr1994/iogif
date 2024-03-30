import imageio
import os

def gif(filenames, out, duration=4):
  images = list(map(lambda filename: imageio.imread(filename), filenames))
  imageio.mimsave(os.path.join(out), images, 'GIF', duration=duration)
