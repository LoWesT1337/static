import os
import shutil
from textnode import TextNode, TextType

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

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # The static directory is the parent of src
    source_dir = os.path.abspath(os.path.join(current_dir, ".."))
    dest_dir = os.path.join(source_dir, "public")
    #print(source_dir)
    #print(dest_dir)
    copy_static(source_dir, dest_dir)
    #node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    #print(node)


main()