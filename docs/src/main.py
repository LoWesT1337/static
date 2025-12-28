import os
import shutil
from markdown_to_html import markdown_to_html_node
from textnode import TextNode, TextType
import sys

def copy_static(source_dir, dest_dir):
    # If destination exists, delete it completely
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Recreate destination directory
    os.mkdir(dest_dir)

    # Iterate through source directory
    for item in os.listdir(source_dir):
        # Skip the destination folder itself
        if item == os.path.basename(dest_dir):
            continue

        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")

        elif os.path.isdir(source_path):
            print(f"Entering directory: {source_path}")
            # Recursively copy subdirectory
            os.mkdir(dest_path)
            copy_static(source_path, dest_path)

def extract_title(markdown):
    """
    Extract the H1 header from a markdown string.

    Raises:
        ValueError: if no H1 header is found.
    """
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 header found in markdown.")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Read files
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown).to_html()

    # Extract title
    title = extract_title(markdown)

    # Replace placeholders
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Adjust href and src for basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Write final HTML
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(source_path):
            generate_pages_recursive(
                source_path,
                template_path,
                os.path.join(dest_dir_path, entry),
                basepath
            )
        elif os.path.isfile(source_path) and entry.endswith(".md"):
            html_filename = entry.rsplit(".", 1)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, html_filename)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(source_path, template_path, dest_path, basepath)

def main():
    # Get basepath from CLI argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.abspath(os.path.join(current_dir, ".."))  # /static
    content_dir = os.path.join(static_dir, "content")
    docs_dir = os.path.join(static_dir, "docs")  # GitHub Pages uses /docs
    template_path = os.path.join(static_dir, "template.html")

    # Clean docs directory
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)

    # Copy static files
    copy_static(static_dir, docs_dir)

    # Generate pages recursively with basepath
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)


main()