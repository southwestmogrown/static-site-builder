import os, shutil, sys
from textnode import *
from utilities import *



def clean_and_populate_public(src, dest, basepath="/"):

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

def generate_page(from_path, template_path, dest_path, basepath="/"):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  content = None
  template = None
  with open(from_path, "r") as f:
    content = f.read()
    with open(template_path, "r") as f:
      template = f.read()

      title = extract_title(content)
      html_content = markdown_to_html_node(content)
      page = template.replace("{{ Title }}", title)
      page = page.replace("{{ Content }}", html_content.to_html())
      page = page.replace('href="/"', f"href={basepath}")
      page = page.replace('src="/"', f"src={basepath}")

      dir, file = os.path.split(dest_path)
      if not os.path.exists(dir):
        os.makedirs(dir)
      
      with open(dest_path, "w") as np:
        np.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
  src_paths = os.listdir(dir_path_content)

  for path in src_paths:
    new_path = os.path.join(dir_path_content, path)
    new_dest = os.path.join(dest_dir_path, path)
    new_dest_html = new_dest.replace("md", "html")
    if os.path.isfile(new_path):
      generate_page(new_path, template_path, new_dest_html, basepath)
    else:
      generate_pages_recursive(new_path, template_path, new_dest)





def main():
  basepath = sys.argv[1]
  clean_and_populate_public("static", "docs", basepath)
  generate_pages_recursive("content", "template.html", "docs", basepath)







if __name__ == "__main__":
   main()