import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []

  for node in old_nodes:
    if node.text_type == "text(plain)":
      new_nodes.append(node)

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

# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

















































# node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
# node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
# node3 = TextNode("This is text with an _italic_ word", TextType.TEXT)

# new_nodes = split_nodes_delimiter([node1], "`", TextType.CODE)
# new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
# new_nodes3 = split_nodes_delimiter([node3], "_", TextType.ITALIC)

# print(new_nodes)
# print(new_nodes2)
# print(new_nodes3)