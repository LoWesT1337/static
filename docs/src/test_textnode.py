import unittest

from textnode import TextNode, TextType
from splitter import extract_markdown_images, split_nodes_delimiter, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_split_code(self):
        node = TextNode("Use `print()` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        assert result == [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]


    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        assert result == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]


    def test_split_italic(self):
        node = TextNode("_italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        assert result == [
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]


    def test_multiple_nodes(self):
        nodes = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        assert result == nodes


    def test_unmatched_delimiter(self):
        node = TextNode("This is `broken code", TextType.TEXT)

        try:
            split_nodes_delimiter([node], "`", TextType.CODE)
            assert False, "Expected ValueError"
        except ValueError:
            pass

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_split_single_image(self):
        node = TextNode(
            "Here is an ![img](img.png) test",
            TextType.TEXT
        )
        result = split_nodes_image([node])
    
        assert result == [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" test", TextType.TEXT),
        ]


    def test_split_multiple_images(self):
        node = TextNode(
            "![one](1.png) and ![two](2.png)",
            TextType.TEXT
        )
        result = split_nodes_image([node])

        assert result == [
            TextNode("one", TextType.IMAGE, "1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "2.png"),
        ]


    def test_split_single_link(self):
        node = TextNode(
            "Click [here](site.com) now",
            TextType.TEXT
        )
        result = split_nodes_link([node])

        assert result == [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "site.com"),
            TextNode(" now", TextType.TEXT),
        ]


    def test_split_multiple_links(self):
        node = TextNode(
            "[one](1.com) and [two](2.com)",
            TextType.TEXT
        )
        result = split_nodes_link([node])

        assert result == [
            TextNode("one", TextType.LINK, "1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, "2.com"),
        ]


    def test_ignore_non_text_nodes(self):
        node = TextNode("bold", TextType.BOLD)
        assert split_nodes_image([node]) == [node]
        assert split_nodes_link([node]) == [node]


    def test_no_images_or_links(self):
        node = TextNode("Just text", TextType.TEXT)
        assert split_nodes_image([node]) == [node]
        assert split_nodes_link([node]) == [node]


    def test_text_to_textnodes_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        result = text_to_textnodes(text)

        assert result == [
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
        ]

    def test_text_only(self):
        text = "Just plain text"
        assert text_to_textnodes(text) == [
            TextNode("Just plain text", TextType.TEXT)
        ]

    def test_only_formatting(self):
        text = "**bold** _italic_ `code`"
        assert text_to_textnodes(text) == [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

    def test_images_and_links_only(self):
        text = "![img](img.png) [link](url)"
        assert text_to_textnodes(text) == [
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]

    def test_invalid_markdown_raises(self):
        text = "This is **broken"
        try:
            text_to_textnodes(text)
            assert False, "Expected ValueError"
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
