import os, shutil
from textnode import *

def clean_and_populate_public(src, dest):
  if os.path.exists(dest):
    shutil.rmtree(dest)


  os.mkdir(dest)
  
  src_paths = os.listdir(src)
  for path in src_paths:
    new_src = os.path.join(src, path)
    if os.path.isfile(new_src):
      shutil.copy(new_src, dest)
    else:
      new_dest = os.path.join(dest, path)
      clean_and_populate_public(new_src, new_dest)





    

def main():
  clean_and_populate_public("static", "public")








if __name__ == "__main__":
   main()