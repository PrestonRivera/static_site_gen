import os
import shutil
from utils import extract_titles
from markdown_blocks import markdown_to_html_node


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
    if os.path.exists('static'):
        for item in os.listdir('static'):
            s = os.path.join('static', item)
            d = os.path.join('public', item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)

def main():

    clear_public_directory()

    copy_static_files()

    generate_page("content/index.md", "template.html", "public/index.html")



if __name__ == "__main__":
    main()

