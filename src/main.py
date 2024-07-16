import os
import shutil
from textnode import TextNode


def copy_static(src, dest):
    # Ensure the destination directory is clean
    if os.path.exists(dest):
        shutil.rmtree(dest)  # Remove all contents of the destination directory
    os.makedirs(dest)  # Create the destination directory

    # Iterate through the items in the source directory
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        # Check if the item is a file or directory
        if os.path.isfile(src_item):
            shutil.copy(src_item, dest_item)  # Copy file
            print(f"Copied file: {src_item} to {dest_item}")
        elif os.path.isdir(src_item):
            copy_static(src_item, dest_item)  # Recursively copy directory
            print(f"Copied directory: {src_item} to {dest_item}")



def main():
    node = TextNode("This is my text", "bold")
    print(node)

    source_directory = "static"
    destination_directory = "public"
    copy_static(source_directory, destination_directory)


if __name__ == "__main__":
    main()

