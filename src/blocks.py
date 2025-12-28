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