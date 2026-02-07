import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
  def test_to_html_exception(self):
    n = HTMLNode()

    with self.assertRaises(NotImplementedError) as context:
      n.to_html()

  def test_props_to_html(self):
    n = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
    r = n.props_to_html()
    x = "href:'https://www.google.com' target:'_blank' " 
    self.assertEqual(r, x)

  def test_repr(self):
    n = HTMLNode("h1", "Hello World!!!", children=[], props={"href": "https://www.google.com", "target": "_blank"})
    r = n.__repr__()
    x = "HTMLNode(h1, Hello World!!!, [], {'href': 'https://www.google.com', 'target': '_blank'})"
    self.assertEqual(r, x)

  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>") 
  
  def test_leaf_to_html_h1(self):
    node = LeafNode("h1", "It's Exciting!")
    self.assertEqual(node.to_html(), "<h1>It's Exciting!</h1>")

  def test_leaf_with_props(self):
    node = LeafNode("p", "How's it going', props?", props={"class": "headings", "id": "heading_text"})
    self.assertEqual(node.to_html(), "<p class:'headings' id:'heading_text' >How's it going', props?</p>") 

  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")





if __name__ == "__main__":
  unittest.main()