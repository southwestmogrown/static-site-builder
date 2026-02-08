import re
from enum import Enum
from textnode import *
from htmlnode import *

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

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:
        block = block.strip()
        if block == "":
            continue

        lines = block.split("\n")
        clean_lines = [line.strip() for line in lines]
        block = "\n".join(clean_lines)

        blocks.append(block)

    return blocks


class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"



def block_to_block_type(block):
  heading_prefixes = [
    "# ",
    "## ",
    "### ",
    "#### ",
    "##### ",
    "###### ",
  ]
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
  

def detect_heading_type(text):
  if text.startswith("###### "):
      s = text[7:]
      return ["h6", s]
  elif text.startswith("##### "):
      s = text[6:]
      return ["h5", s]
  elif text.startswith("#### "):
      s = text[5:]
      return ["h4", s]
  elif text.startswith("### "):
      s = text[4:]
      return ["h3", s]
  elif text.startswith("## "):
      s = text[3:]
      return ["h2", s]
  elif text.startswith("# "):
      s = text[2:]
      return ["h1", s]
  else:
      raise Exception("Invalid Markdown")
  
def text_to_html_nodes(text):
  text_nodes = text_to_text_nodes(text)
  html_nodes = [text_node_to_html_node(node) for node in text_nodes]
  return html_nodes
  
def handle_paragraphs(block):
    lines = block.split("\n")
    clean_lines = [line.strip() for line in lines if line.strip() != ""]
    paragraph_text = " ".join(clean_lines)
    html_nodes = text_to_html_nodes(paragraph_text)
    block_node = ParentNode("p", children=html_nodes)
    return block_node

def handle_headings(block):
  tag, text = detect_heading_type(block)
  html_nodes = text_to_html_nodes(text)

  block_node = ParentNode(tag, children=html_nodes)
  return block_node

def handle_quotes(block):
  block = block[1:].strip()
  html_nodes = text_to_html_nodes(block)
  block_node = ParentNode("blockqoute", children=html_nodes)
  return block_node

def handle_lists(block):
  bt = block_to_block_type(block)
  tag = "ol" if bt is BlockType.ORDERED_LIST else "ul"
  lines = block.split("\n")
  if bt is BlockType.UNORDERED_LIST:
     lines = [line[2:] for line in lines]

  clean_lines = [line.strip() for line in lines if line != ""]
  html_nodes = [text_to_html_nodes(line)[0] for line in clean_lines if line != ""]
  li_nodes = []
  for node in html_nodes:
      li = ParentNode("li", children=[])
      li.children.append(node)
      li_nodes.append(li)
  
  
  block_node = ParentNode(tag, li_nodes)
  return block_node

def handle_code(block):
  lines = block.strip().split("\n")
  txt = "\n".join(lines)
  t_node = TextNode(txt[4:-3], text_type=TextType.TEXT)
  html_node = text_node_to_html_node(t_node)
  code_node = ParentNode("code", [html_node])
  block_node = ParentNode("pre", [code_node])
  return block_node


def markdown_to_html_node(markdown):
  html = ParentNode("div", [])
  blocks = markdown_to_blocks(markdown)

  for block in blocks:
      bt = block_to_block_type(block)
      match bt:
          case BlockType.PARAGRAPH:
            block_node = handle_paragraphs(block)
            html.children.append(block_node)
          case BlockType.HEADING:
            block_node = handle_headings(block)
            html.children.append(block_node)
          case BlockType.QUOTE:
            block_node = handle_quotes(block)
            html.children.append(block_node)
          case BlockType.ORDERED_LIST:
            block_node = handle_lists(block)
            html.children.append(block_node)
          case BlockType.UNORDERED_LIST:
            block_node = handle_lists(block)
            html.children.append(block_node)
          case BlockType.CODE:
            block_node = handle_code(block)
            html.children.append(block_node)

  return html
      
    





# md = """

#   This is **bolded** paragraph
#   text in a p
#   tag here

#   This is another paragraph with _italic_ text and `code` here

#   ###### This is an h6

#   ## This is an h2

#   # And an h1 for good measure

#   >This is a quote block without the space

#   > This is a qoute block with the space added


#   1. This
#   2. is
#   3. an
#   4. ordered
#   5. list

#   - This
#   - is
#   - an
#   - unordered
#   - list

#   ```
#   This is text that _should_ remain
#   the **same** even with inline stuff
#   ```

#   """

# node = markdown_to_html_node(md)
# print(node.to_html())