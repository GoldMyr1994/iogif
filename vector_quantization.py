import numpy as np
import cv2

def split_centroid(c,v):
  c1 = np.asarray([min(e,255.) for e in c+v])
  c2 = np.asarray([max(e,0.) for e in c-v])
  return (c1, c2)

def split_centroids(cen,v):
  centroids = []
  for c in cen:
      centroids.extend(split_centroid(c,1))
  return centroids

def map_centroids( img, centroids ):
  map_img = np.zeros((img.shape[0],img.shape[1]),np.uint8)
  q_img = np.zeros_like(img)
  MSE = 0
  for i in range(img.shape[0]):
    for j in  range(img.shape[1]):
      distances = [ np.sum(np.power(np.subtract(img[i,j,:],c),2)) for c in centroids ]
      map_img[i,j] = distances.index(min(distances))
      q_img[i,j] = centroids[map_img[i,j]]
      MSE +=  distances[map_img[i,j]]
  MSE = MSE/(img.shape[0]*img.shape[1])

  return q_img, map_img, MSE

def move_centroids(img, map_img, centroids):
  new_centroids = [ 0.0 for e in centroids ]
  cnt_centroids = [ 0 for e in centroids ]
  for i in range(img.shape[0]):
    for j in  range(img.shape[1]):
      new_centroids[map_img[i,j]] += img[i,j]
      cnt_centroids[map_img[i,j]] += 1
  return [new_centroids[i]/cnt_centroids[i] for i in range(len(new_centroids))]


def LGB( img, l, centroids = [ ] ):
  img = img.astype(np.float64)
  if len(centroids) == 0:
    centroids.append( np.mean(img,axis=(0,1),dtype=np.float64) )
  while len(centroids) < l:
    centroids = split_centroids(centroids,1)
    print("#centroids:", len(centroids))
    q_img, map_matrix, MSE = map_centroids( img, centroids )
    MSE_prev = MSE + 1000
    while (MSE_prev-MSE)>100:
      print('decreasing MSE...')
      MSE_prev = MSE
      centroids = move_centroids(img, map_matrix, centroids)
      q_img, map_matrix, MSE = map_centroids( img, centroids )
  return q_img.astype(np.uint8), centroids, map_matrix

# def main():
#   img = cv2.imread('images-3.jpeg')
#   q, centroids, map_img = LGB(img,4)
#   cv2.imwrite('out/test_vector_quantization.png', q)

# if __name__ == 'main':
#     main()

