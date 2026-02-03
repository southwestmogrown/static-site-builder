from textnode import *

class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError("Not implemented!!!")
  
  def props_to_html(self):
    if self.props is None:
      return ""
    
    s = ""

    for prop in self.props:
      s += f"{prop}:'{self.props[prop]}' "
    
    return s
  
  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
class LeafNode(HTMLNode):
  
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, props)
    self.props = props

  def to_html(self):
    if not self.value:
      raise ValueError("All leaf nodes must have a value!")
    if self.tag is None:
      return f"{self.value}"
    
    str = ""
    if self.props is not None:
      str += f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
    else:
      str += f"<{self.tag}>{self.value}</{self.tag}>"

    
    
    return str
    
  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.props})" 


class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, children, props)
    self.children = children
    self.props = props

  def to_html(self):

    if self.tag is None:
      raise ValueError("All parent nodes must have tags!")
    if self.children is None:
      raise ValueError("All parent nodes must have children!")
    
    pStart = f"<{self.tag}>"
    pEnd = f"</{self.tag}>"

    for child in self.children:
      res = child.to_html()
      pStart += res
    return pStart + pEnd
  

def text_node_to_html_node(text_node):
  tt = text_node.text_type
  match (tt):
    case TextType.PLAIN:
      n = LeafNode(None, text_node.text)
      return n
    case TextType.BOLD:
      n = LeafNode('b', text_node.text)
      return n
    case TextType.ITALIC:
      n = LeafNode('i', text_node.text)
      return n
    case TextType.CODE:
      n = LeafNode('code', text_node.text)
      return n
    case TextType.LINK:
      n = LeafNode('a', text_node.text, props={"href": text_node.url})
      return n
    case TextType.IMAGE:
      n = LeafNode('img', '', props={"src": text_node.url, "alt": text_node.text})
      return n
    case _:
      raise Exception("Must use valid text type")


# tn = TextNode("hello world", TextType.PLAIN)

# print(text_node_to_html_node(tn))