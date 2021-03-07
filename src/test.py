import sys
sys.path.append('/Users/mauroconte/Desktop/iogif/')
import util

def get_lena():
  util.read_image_from_url('https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/440px-Lenna_%28test_image%29.png')
  

def get_billie():
  util.read_image_from_url('https://assets.vogue.com/photos/5e40a7942f0ba000086d7dd9/master/w_2560%2Cc_limit/billie-eilish-social.jpg')

def main():
  get_billie()

if __name__ == "__main__":
  main()