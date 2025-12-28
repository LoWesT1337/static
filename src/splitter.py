from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # If delimiter count is even, there's no matching closing delimiter
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text: {node.text}"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                # Outside delimiter → normal text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Inside delimiter → given text_type
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text)
    return matches

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        remaining_text = text

        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            before, remaining_text = remaining_text.split(image_markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        remaining_text = text

        for anchor, url in links:
            link_markdown = f"[{anchor}]({url})"
            before, remaining_text = remaining_text.split(link_markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Order matters!
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes