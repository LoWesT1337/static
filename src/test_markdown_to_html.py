import unittest
from markdown_to_html import *

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html_single_paragraph(self):
        md = "This is **bold** text"
    
        node = markdown_to_html_node(md)
        html = node.to_html()
    
        assert html == (
            "<div>"
            "<p>"
            "This is <b>bold</b> text"
            "</p>"
            "</div>"
        )

    def test_markdown_to_html_multiple_blocks(self):
        md = """
# Heading

This is a paragraph

- Item one
- Item two
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
    
        assert html == (
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph</p>"
            "<ul>"
            "<li>Item one</li>"
            "<li>Item two</li>"
            "</ul>"
            "</div>"
        )

    def test_markdown_to_html_code_block(self):
        md = """
```print("hello")```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == (
            "<div>"
            "<pre><code>print(\"hello\")</code></pre>"
            "</div>"
        )

    def test_markdown_to_html_quote(self):
        md = """
> This is a quote
> with two lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        assert html == (
            "<div>"
            "<blockquote>This is a quote\nwith two lines</blockquote>"
            "</div>"
        )

def test_markdown_to_html_ordered_list(self):
    md = """
1. First
2. Second
3. Third
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    assert html == (
        "<div>"
        "<ol>"
        "<li>First</li>"
        "<li>Second</li>"
        "<li>Third</li>"
        "</ol>"
        "</div>"
    )


