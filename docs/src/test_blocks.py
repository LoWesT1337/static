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

    def test_heading_block(self):
        assert block_to_block_type("# Heading") == BlockType.HEADING
        assert block_to_block_type("###### Heading") == BlockType.HEADING

    def test_not_heading_no_space(self):
        assert block_to_block_type("##Heading") == BlockType.PARAGRAPH

    def test_code_block(self):
        block = "```\ncode here\n```"
        assert block_to_block_type(block) == BlockType.CODE

    def test_not_code_block(self):
        block = "```\ncode here"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_quote_block(self):
        block = "> Quote line one\n> Quote line two"
        assert block_to_block_type(block) == BlockType.QUOTE

    def test_mixed_quote_not_quote(self):
        block = "> Quote line\nNormal line"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        assert block_to_block_type(block) == BlockType.UNORDERED_LIST

    def test_unordered_list_missing_space(self):
        block = "-item one\n- item two"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        assert block_to_block_type(block) == BlockType.ORDERED_LIST

    def test_ordered_list_wrong_order(self):
        block = "1. first\n3. second"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_ordered_list_not_starting_at_one(self):
        block = "2. first\n3. second"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_ordered_list_not_starting_at_one(self):
        block = "2. first\n3. second"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_multiline_paragraph(self):
        block = "Line one\nLine two"
        assert block_to_block_type(block) == BlockType.PARAGRAPH