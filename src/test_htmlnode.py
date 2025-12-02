import unittest

from htmlnode import HTMLNode

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