import re
from enum import Enum
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []

  for node in old_nodes:
    if node.text_type != TextType.TEXT or delimiter not in node.text:
      new_nodes.append(node)
      continue

    try:
      
      pre, delimited, post = node.text.split(delimiter)
    except:
      raise Exception("Invalid Markdown")
    

    n1 = TextNode(pre, TextType.TEXT)
    n2 = TextNode(delimited, text_type)
    n3 = TextNode(post, TextType.TEXT)

    new_nodes.extend([n1, n2, n3])

  return new_nodes


def extract_markdown_images(text):
  matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return matches


def extract_markdown_links(text):
  matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return matches

def split_nodes_image(old_nodes):
  new_nodes = []

  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue

    images = extract_markdown_images(node.text)
    str = node.text

    for image in images:
      b, _d, a = str.partition(f"![{image[0]}]({image[1]})")
      new_nodes.append(TextNode(b, TextType.TEXT))
      new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
      str = a
    if str != "":
      new_nodes.append(TextNode(str, TextType.TEXT))
  return new_nodes
      

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:

    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue

    links = extract_markdown_links(node.text)
    str = node.text

    for link in links:
      b, _d, a = str.partition(f"[{link[0]}]({link[1]})")
      new_nodes.append(TextNode(b, TextType.TEXT))
      new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
      str = a

    if str != "":
      new_nodes.append(TextNode(str, TextType.TEXT))

  return new_nodes

def text_to_text_nodes(text):
  n = TextNode(text, TextType.TEXT)

  links_handled = split_nodes_link([n])
  img_handled = split_nodes_image(links_handled)
  bold = split_nodes_delimiter(img_handled, "**", TextType.BOLD)
  italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
  code = split_nodes_delimiter(italic, "`", TextType.CODE)

  return code

def markdown_to_blocks(md):
  s = md.split("\n\n")

  s = [x.strip() for x in s]

  for i in range(len(s)):
    block = s[i]

    if block != "":
      lines = block.split("\n")

      clean_lines = [line.strip() for line in lines]

      s[i] = "\n".join(clean_lines)
  return s


class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

heading_prefixes = [
  "# ",
  "## ",
  "### ",
  "#### ",
  "##### ",
  "###### ",
]

def block_to_block_type(block):
  for pf in heading_prefixes:
    if block.startswith(pf):
      return BlockType.HEADING
  
  if block.startswith("```") and block.endswith("```"):
    return BlockType.CODE
  
  if block.startswith(">") or block.startswith("> "):
    return BlockType.QUOTE
  
  if block.startswith("- "):
    return BlockType.UNORDERED_LIST
  
  if block.startswith("1. "):
    lines = block.split("\n")
    is_O_list = True

    for i in range(0, len(lines)):
      line = lines[i]
      if not line.startswith(f"{i+1}. "):
        is_O_list = False
    
    return BlockType.ORDERED_LIST if is_O_list is True else BlockType.PARAGRAPH
  
  return BlockType.PARAGRAPH
  

# h = """
# 1. this
# 2. is
# 3. an
# 4. ordered
# 5. list
# """
# h = markdown_to_blocks(h)
# print(h)
# print(block_to_block_type(h[0]))