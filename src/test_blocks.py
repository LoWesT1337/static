import unittest
from blocks import *


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        assert blocks == [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

    def test_single_block(self):
        md = "Just one paragraph"
        assert markdown_to_blocks(md) == ["Just one paragraph"]

    def test_extra_newlines(self):
        md = "\n\nParagraph one\n\n\n\nParagraph two\n\n"
        assert markdown_to_blocks(md) == [
            "Paragraph one",
            "Paragraph two",
        ]

    def test_list_block(self):
        md = """
- item one
- item two
- item three
"""
        assert markdown_to_blocks(md) == [
            "- item one\n- item two\n- item three"
        ]
    
    def test_heading_and_paragraph(self):
        md = """
        # Heading

        This is a paragraph.
        """
        assert markdown_to_blocks(md) == [
            "# Heading",
            "This is a paragraph.",
        ]


