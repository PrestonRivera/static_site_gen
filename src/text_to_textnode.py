from textnode import TextNode
from extractors import extract_markdown_images, extract_markdown_links
from textnode_splitter import split_bold, split_italic, split_code


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_image = "image"
text_type_link = "link"


def text_to_textnode(text):
    new_textnodes = []

    image_segments = extract_markdown_images(text)
    

    link_segments = []

    for segment in image_segments:
        if isinstance(segment, TextNode) and segment.text_type == text_type_text:
            link_segments.extend(extract_markdown_links(segment.text) or [])
        else:
            link_segments.append(segment)

    for segment in link_segments:
        if isinstance(segment, TextNode) and segment.text_type == text_type_text:
            bold_nodes = split_bold(segment.text) or []
            for bold_node in bold_nodes:
                if bold_node.text_type == text_type_text:
                    italic_nodes = split_italic(bold_node.text) or []
                    for italic_node in italic_nodes:
                        if italic_node.text_type == text_type_text:
                            code_nodes = split_code(italic_node.text) or []
                            new_textnodes.extend(code_nodes)
                        else:
                            new_textnodes.append(italic_node)
                else:
                    new_textnodes.append(bold_node)
        else:
            new_textnodes.append(segment)

    merged_textnodes = []
    for node in new_textnodes:
        if merged_textnodes and merged_textnodes[-1].text_type == text_type_text and node.text_type == text_type_text:
            merged_textnodes[-1].text += node.text
        else:
            merged_textnodes.append(node)

    return merged_textnodes

