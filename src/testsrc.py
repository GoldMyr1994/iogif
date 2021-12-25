import sys
sys.path.append('/Users/mauroconte/Desktop/iogif/')
import util

def get_io(): 
  return util.read_image_from_disk('src/io.png')

def get_lena():
  return util.read_image_from_url('https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/440px-Lenna_%28test_image%29.png')
  
def get_billie():
  return util.read_image_from_url('https://media.gqitalia.it/photos/6089331d8a8620fb02fad5ba/1:1/w_960,c_limit/Billie%20Eilish_cover%20album%20Happier%20Than%20Ever.jpg')