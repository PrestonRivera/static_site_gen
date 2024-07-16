from textnode import TextNode
from extractors import extract_markdown_images, extract_markdown_links


def split_nodes_images(old_nodes):
    image_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == "text":
            if old_node.text == "":
                image_nodes.append(TextNode("", "text"))
                continue

            image_segments = extract_markdown_images(old_node.text)
            image_nodes.extend(image_segments)
        else:
            image_nodes.append(old_node)
    return image_nodes

def split_nodes_links(old_nodes):
    link_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == "text":
            if old_node.text == "":
                link_nodes.append(TextNode("", "text"))
                continue

            link_segments = extract_markdown_links(old_node.text)
            link_nodes.extend(link_segments)
        else:
            link_nodes.append(old_node)
    return link_nodes
                


if __name__ == "__main__":


    # Sample textnode objects
    test_text_nodes = [TextNode("This is an ![image](https://example.com/image.png) and a [link](https://example.com)", "text")]

    # Run split_nodes_images
    result_images = split_nodes_images(test_text_nodes)
    print("Result images:", result_images)
    for node in result_images:
        print(node.text, node.text_type, getattr(node, 'link', None))

    # Run split_nodes_links
    result_links = split_nodes_links(result_images)
    print("Result links:", result_links)
    for node in result_links:
        print(node.text, node.text_type, getattr(node, 'link', None))