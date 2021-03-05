import numpy as np
import cv2
import os

module = 64
n = 9

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
