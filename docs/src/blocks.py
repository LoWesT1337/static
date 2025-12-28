from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading: 1–6 '#' followed by a space
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Code block: starts and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote block: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines start with 1. 2. 3. ...
    ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    # Default
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    """
    Splits a markdown document into blocks separated by blank lines.
    """
    # Split on double newlines
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped:
            blocks.append(stripped)

    return blocks