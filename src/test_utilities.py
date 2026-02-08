import unittest
from utilities import *
from textnode import *


class TestExtraction(unittest.TestCase):
  def test_split_nodes_delimiter(self):
    node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
    node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
    node3 = TextNode("This is text with an _italic_ word", TextType.TEXT)

    new_nodes = split_nodes_delimiter([node1], "`", TextType.CODE)
    new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
    new_nodes3 = split_nodes_delimiter([node3], "_", TextType.ITALIC)

    self.assertListEqual([TextNode("This is text with a " , TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" word", TextType.TEXT, None)], new_nodes)
    self.assertListEqual([TextNode("This is text with a ", TextType.TEXT, None), TextNode("bold", TextType.BOLD, None), TextNode(" word", TextType.TEXT, None)], new_nodes2)
    self.assertListEqual([TextNode("This is text with an ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None), TextNode(" word", TextType.TEXT, None)], new_nodes3)



  def test_extract_markdown_images(self):
      matches = extract_markdown_images(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
      )
      self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_links(self):
     matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev)"
     )

     self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

  def test_split_link(self):
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
    )

  def test_text_to_text_nodes(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ], text_to_text_nodes(text))

  def test_markdown_to_blocks(self):
    md = """
      This is **bolded** paragraph

      This is another paragraph with _italic_ text and `code` here
      This is the same paragraph on a new line

      - This is a list
      - with items
    """
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

  def test_block_to_block_type_headings(self):
    headings = [
      "# h1",
      "## h2",
      "### h3",
      "#### h4",
      "##### h5",
      "###### h6",
    ]

    res = []

    for heading in headings:
      res.append(block_to_block_type(heading))

    self.assertListEqual([
      BlockType.HEADING, 
      BlockType.HEADING, 
      BlockType.HEADING, 
      BlockType.HEADING, 
      BlockType.HEADING, 
      BlockType.HEADING,
    ], res)

  def test_block_to_block_type_headings_bad(self):
    headings = [
      "#h1",
      "## h2",
      "### h3",
      "#### h4",
      "#####h5",
      "###### h6",
    ]

    res = []

    for heading in headings:
      res.append(block_to_block_type(heading))

    self.assertListEqual([
      BlockType.PARAGRAPH, 
      BlockType.HEADING, 
      BlockType.HEADING, 
      BlockType.HEADING, 
      BlockType.PARAGRAPH, 
      BlockType.HEADING,
    ], res)