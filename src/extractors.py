import re
from textnode import TextNode



text_type_image = "image"
text_type_link = "link"
text_type_text = "text" 

def extract_markdown_images(text):
    extract_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    segments = []
    last_index = 0

    for match in extract_images:
        alt_text, url = match
        start_idx = text.find(f"![{alt_text}]({url})", last_index)
        if start_idx != last_index:
            segments.append(TextNode(text[last_index:start_idx], text_type_text))
        segments.append(TextNode(alt_text, text_type_image, url))
        last_index = start_idx + len(f"![{alt_text}]({url})")

    if last_index < len(text):
        segments.append(TextNode(text[last_index:], text_type_text))

    return segments

def extract_markdown_links(text):
    extract_links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    segments = []
    last_index = 0

    for match in extract_links:
        link_text, url = match
        start_idx = text.find(f"[{link_text}]({url})", last_index)
        if start_idx != last_index:
            segments.append(TextNode(text[last_index:start_idx], text_type_text))
        segments.append(TextNode(link_text, text_type_link, url))
        last_index = start_idx + len(f"[{link_text}]({url})")

    if last_index < len(text):
        segments.append(TextNode(text[last_index:], text_type_text))

    return segments
