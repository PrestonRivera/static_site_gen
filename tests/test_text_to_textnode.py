from textnode import TextNode
from textnode_splitter import split_nodes_delimiter, split_bold, split_italic, split_code
from text_to_textnode import text_to_textnode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_image, text_type_link

def test_correct_split():
    old_nodes = [TextNode("This is *italic* text", text_type_text)]
    new_nodes = split_nodes_delimiter(old_nodes, "*", text_type_italic)

    expected_nodes = [
        TextNode("This is ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" text", text_type_text)
    ]

    assert new_nodes == expected_nodes, f"Expected {expected_nodes} but got {new_nodes}"
    print("Test Passed: correct split")

def test_unclosed_delimiter():
    old_nodes = [TextNode("This is *italic text", text_type_text)]
    try:
        split_nodes_delimiter(old_nodes, "*", text_type_italic)
    except ValueError as e:
        print(f"Caught expected exception: {e}")
    else:
        print("Test Failed: expected exception for unclosed delimiter")

# Tests for split_bold, split_italic, split_code
def test_split_bold():
    text = "This is **bold** text"
    expected_nodes = [
        TextNode("This is ", text_type_text),
        TextNode("bold", text_type_bold),
        TextNode(" text", text_type_text)
    ]
    bold_nodes = split_bold(text)
    assert bold_nodes == expected_nodes, f"Expected {expected_nodes} but got {bold_nodes}"
    print("Test Passed: split bold")

def test_split_italic():
    text = "This is *italic* text"
    expected_nodes = [
        TextNode("This is ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" text", text_type_text)
    ]
    italic_nodes = split_italic(text)
    assert italic_nodes == expected_nodes, f"Expected {expected_nodes} but got {italic_nodes}"
    print("Test Passed: split italic")

def test_split_code():
    text = "This is `code` text"
    expected_nodes = [
        TextNode("This is ", text_type_text),
        TextNode("code", text_type_code),
        TextNode(" text", text_type_text)
    ]
    code_nodes = split_code(text)
    assert code_nodes == expected_nodes, f"Expected {expected_nodes} but got {code_nodes}"
    print("Test Passed: split code")

def test_text_to_textnode():
    text = "This is **bold** and *italic* text with `code` and an ![image](https://example.com/image.jpg) and a [link](https://example.com)."
    expected_nodes = [
        TextNode("This is ", text_type_text),
        TextNode("bold", text_type_bold),
        TextNode(" and ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" text with ", text_type_text),
        TextNode("code", text_type_code),
        TextNode(" and an ", text_type_text),
        TextNode("image", text_type_image, "https://example.com/image.jpg"),
        TextNode(" and a ", text_type_text),
        TextNode("link", text_type_link, "https://example.com"),
        TextNode(".", text_type_text)  # Expected trailing punctuation as separate node
    ]

    result_nodes = text_to_textnode(text)
    
    print(f"Expected Nodes: {expected_nodes}")
    print(f"Result Nodes: {result_nodes}")
    
    assert result_nodes == expected_nodes, f"Expected {expected_nodes} but got {result_nodes}"
    print("Test Passed: text_to_textnode")

def main():
    test_correct_split()
    test_unclosed_delimiter()
    test_split_bold()
    test_split_italic()
    test_split_code()
    test_text_to_textnode()

if __name__ == "__main__":
    main()