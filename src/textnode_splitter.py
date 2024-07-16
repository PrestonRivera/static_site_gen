from textnode import TextNode



text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"



def split_nodes_delimiter(old_nodes, delimiter, new_text_type):
   
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(f"Mismatched delimiter: '{delimiter}' in text '{old_node.text}'")
            for i, part in enumerate(parts):
                if part: # Not an empty string
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, "text"))
                    else:
                        new_nodes.append(TextNode(part, new_text_type))
    return new_nodes


def split_bold(text):
    parts = text.split('**')
    nodes = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            nodes.append(TextNode(part, "text"))
        else:
            nodes.append(TextNode(part, "bold"))
    return nodes


def split_italic(text):
    parts = text.split('*')
    nodes = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            nodes.append(TextNode(part, "text"))
        else:
            nodes.append(TextNode(part, "italic"))
    return nodes


def split_code(text):
    parts = text.split('`')
    nodes = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            nodes.append(TextNode(part, "text"))
        else:
            nodes.append(TextNode(part, "code"))
    return nodes



                

if __name__ == "__main__":


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
            print("Caught expected exception", e)
        else:
            print("Test Failed: expected exception for unclosed delimter")

    
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
        print("Test passed: split code")


    test_correct_split()
    test_unclosed_delimiter()
    test_split_bold()
    test_split_italic()
    test_split_code()
    