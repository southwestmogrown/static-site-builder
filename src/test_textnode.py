import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_bad_input(self):
        node = TextNode("This is the first text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_custom_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        res = node.__eq__(node2)
        self.assertTrue(res)

    def test_custom_eq_bad(self):
        node = TextNode("This is the first text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.ITALIC)
        res = node.__eq__(node2)
        self.assertFalse(res)
    
    def test_repr(self):
        node = TextNode("This is the first text node", TextType.BOLD)
        self.assertEqual(node.__repr__(), "TextNode(This is the first text node, **Bold text**, None)")

if __name__ == "__main__":
    unittest.main()