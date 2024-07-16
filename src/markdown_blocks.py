import re
from text_to_textnode import text_to_textnode
from htmlnode import ParentNode, text_node_to_html_node


def markdown_to_block(markdown):
    block_strings = []
    separated_block = markdown.split("\n\n")
    
    for block in separated_block:
        stripped_block = block.strip()
        if stripped_block:
            block_strings.append(stripped_block)
    return block_strings 

            



def block_to_block_type(block):
    # The regular expression ^\#{1,6} ensures that the line starts with 1-6 # characters followed by a space
    if re.match(r'^\#{1,6} ', block):
        return "heading"
    
    # Check for code if block.startswith("```") and block.endswith("```") checks if the block starts and ends with triple backticks
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    # Check for quote block if all(line.startswith('> ') for line in block.split('\n')) checks if every line starts with > 
    if all(line.startswith('> ') for line in block.split('\n')):
        return "quote"
    
    # Check for unordered list block if all(line.startswith(('* ', '- ')) for line in block.split('\n')) checks if every line starts with * or - 
    if all(line.startswith(('* ', '- ')) for line in block.split('\n')):
        return "unordered list"
    
    # Check for ordered list block if all(re.match(r'^\d+\. ', line) for line in block.split('\n')) checks if every line starts with a number followed by a . 
    if all(re.match(r'^\d+\. ', line) for line in block.split('\n')):
        return "ordered list"
    
    # If none of the above, it's a paragraph
    return "paragraph"


def markdown_to_html_node(markdown):
    split_md = markdown_to_block(markdown.strip())
    html_nodes = []

    for block in split_md:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            node = heading_to_html_node(block)
        elif block_type == "code":
            node = code_to_html_node(block)
        elif block_type == "quote":
            node = quote_to_html_node(block)
        elif block_type == "unordered list":
            node = ulist_to_html_node(block)
        elif block_type == "ordered list":
            node = olist_to_html_node(block)
        else:
            node = paragraph_to_html_node(block)

        html_nodes.append(node)
    return ParentNode("div", html_nodes)


def text_to_children(text):
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines).strip()
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.rstrip().endswith("```"):
        raise ValueError("Invalid code block")
    text = block[3:-3].strip()
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_paragraphs = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        content = line.lstrip("> ").strip()
        paragraph_node = ParentNode("p", text_to_children(content))
        new_paragraphs.append(paragraph_node)
    return ParentNode("blockquote", new_paragraphs)
