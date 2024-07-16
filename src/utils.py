import os
import shutil


def extract_titles(markdown):
    if "#" not in markdown:
        raise Exception("No header to remove")
    
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()

    raise Exception("No h1 header found")


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




if __name__ == "__main__":

    source_directory = "static"
    destination_directory = "public"
    copy_static(source_directory, destination_directory)