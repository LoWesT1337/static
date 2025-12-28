import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello", [], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html_empty(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode("div", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        node = HTMLNode("div", props={"class": "container", "data-role": "page"})
        props_html = node.props_to_html()
        self.assertIn(' class="container"', props_html)
        self.assertIn(' data-role="page"', props_html)

    def test_props_to_html_single(self):
        node = HTMLNode("div", props={"id": "main"})
        self.assertEqual(node.props_to_html(), ' id="main"')

    def test_repr(self):
        node = HTMLNode("div", "Hello", [], {"class": "container"})
        expected_repr = "HTMLNode(tag=div, value=Hello, children=[], props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click here", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click here</a>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p",None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_with_props(self):
        node = LeafNode("img", None, {"src": "image.png", "alt": "An image"})
        with self.assertRaises(ValueError):
            node.to_html()

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

    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>",
        )   

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("print('Hello, world!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, world!')")

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image"})