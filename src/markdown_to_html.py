from splitter import *
from blocks import *
from htmlnode import *
from textnode import *

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # Heading
        if block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])
            text = block[level + 1:]
            children.append(
                ParentNode(f"h{level}", text_to_children(text))
            )

        # Paragraph
        elif block_type == BlockType.PARAGRAPH:
            children.append(
                ParentNode("p", text_to_children(block))
            )

        # Quote
        elif block_type == BlockType.QUOTE:
            quote_text = "\n".join(
                line[1:].lstrip() for line in block.split("\n")
            )
            children.append(
                ParentNode("blockquote", text_to_children(quote_text))
            )

        # Unordered list
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                text = line[2:]
                items.append(
                    ParentNode("li", text_to_children(text))
                )
            children.append(
                ParentNode("ul", items)
            )

        # Ordered list
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                text = line.split(". ", 1)[1]
                items.append(
                    ParentNode("li", text_to_children(text))
                )
            children.append(
                ParentNode("ol", items)
            )

        # Code block (special case: no inline parsing)
        elif block_type == BlockType.CODE:
            code_text = block[3:-3].strip("\n")
            code_node = text_node_to_html_node(
                TextNode(code_text, TextType.TEXT)
            )
            children.append(
                ParentNode("pre", [ParentNode("code", [code_node])])
            )

        else:
            raise ValueError("Unknown block type")

    return ParentNode("div", children)
