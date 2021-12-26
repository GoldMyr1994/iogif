import sys
sys.path.append('/Users/mauroconte/Desktop/iogif/')
import util
import cv2
import numpy as np
import vector_quantization

scale = 10

iobase = util.read_image_from_disk('src/iosquare.png', 3*scale)
iobase = iobase[:,:,:3]
iobase = vector_quantization.LGB(iobase, 4)[0]

def get_bright():
  tmp = np.zeros(iobase.shape, dtype=np.uint8) + 255
  while np.mean(tmp)<175 or np.mean(tmp)>225:
    tmp = util.colormap(iobase, [np.random.randint(155,255,size=3) for i in range(int(4))])
  tmp = np.mean(tmp, axis=2).astype(np.uint8)
  return tmp

def get_dark():
  tmp = np.zeros(iobase.shape, dtype=np.uint8) + 255
  while np.mean(tmp)<25 or np.mean(tmp)>75:
    tmp = util.colormap(iobase, [np.random.randint(0,100,size=3) for i in range(int(4))])
  tmp = np.mean(tmp, axis=2).astype(np.uint8)
  return tmp

def main():
  img = util.read_image_from_disk('src/greenpass.png', None)

  img = img[10:, 10:]
  img = img[:-10, :-10]
  h, w = img.shape
  dy, dx = 3, 3
  rows, cols = h//dy, w//dx

  newqr = np.zeros((rows*dy*scale, cols*dx*scale), dtype=np.uint8)

  for y in np.arange(0, h, dy):
    for x in np.arange(0, w, dx):
      original_square = img[y:y+dy, x:x+dx]
      is_bright = np.sum(original_square.astype(np.uint8))
      if is_bright == 0:
        newqr[y*scale:y*scale+dy*scale, x*scale:x*scale+dx*scale] = get_dark()
      elif is_bright == 9:
        newqr[y*scale:y*scale+dy*scale, x*scale:x*scale+dx*scale] = get_bright()
      else:
        newqr[y*scale:y*scale+dy*scale, x*scale:x*scale+dx*scale] = 127
  n = np.zeros((newqr.shape[0]+2*10*scale, newqr.shape[1]+2*10*scale), np.uint8)+255
  n[10*scale:n.shape[0]-10*scale, 10*scale:n.shape[1]-10*scale] = newqr[:,:]
  cv2.imwrite('regenerated-qrcode.png', n.astype(np.uint8))

if __name__ == '__main__':
  print(f'runnning {__file__}')
  main()
