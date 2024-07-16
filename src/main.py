import os
import shutil
from utils import extract_titles
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Crawling directory: {dir_path_content} to generate in {dest_dir_path}")

    for entry in os.listdir(dir_path_content):
        full_entry_path = os.path.join(dir_path_content, entry)
        print(f"Processing entry: {full_entry_path}")

        if os.path.isfile(full_entry_path) and full_entry_path.endswith('.md'):
            print(f"Markdown file found: {full_entry_path}")

            # Calculate relative path from the content directory root
            relative_path = os.path.relpath(full_entry_path, "content")
            html_dest_path = os.path.join(dest_dir_path, relative_path).replace('.md', '.html')

            print(f"HTML destination path: {html_dest_path}")

            # Ensure the destination directory exists
            dest_dir = os.path.dirname(html_dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
                print(f"Created directory: {dest_dir}")

            # Call generate_page to create the HTML file
            generate_page(full_entry_path, template_path, html_dest_path)

        elif os.path.isdir(full_entry_path):
            print(f"Entering directory: {full_entry_path}")

            # Recursive call for the subdirectory
            generate_pages_recursive(full_entry_path, template_path, dest_dir_path)



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content)  # Directly get the HTML content

    # Extract the title
    title = extract_titles(markdown_content)

    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Write the final HTML content to the destination path
    with open(dest_path, 'w') as f:
        f.write(final_html)


def clear_public_directory():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public", exist_ok=True)


def copy_static_files():
    if os.path.exists("static"):
        for item in os.listdir("static"):
            s = os.path.join("static", item)
            d = os.path.join("public", item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)

def main():

    clear_public_directory()
    copy_static_files()

    generate_pages_recursive("content", "template.html", "public")

    print("Site generation complete.")


if __name__ == "__main__":
    main()

