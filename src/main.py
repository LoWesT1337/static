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
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")

        else:
            print(f"Entering directory: {source_path}")
            copy_static(source_path, dest_path)

def main():
    copy_static("static", "public")
    #node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    #print(node)


main()