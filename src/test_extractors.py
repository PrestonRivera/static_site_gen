from extractors import extract_markdown_links, extract_markdown_images
from textnode import TextNode

def test_extract_markdown_images():
    text = "this is text with a image ![rick roll](https://i.imgur.com/aKaOqIH.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    expected_output = [
        TextNode("this is text with a image ", "text", None),
        TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIH.gif"),
        TextNode(" and ", "text", None),
        TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
    ]
    actual_output = extract_markdown_images(text)
    print("Actual output:", actual_output)
    print("Expected output:", expected_output)
    assert actual_output == expected_output
    print("extract_markdown_images works!")

def test_extract_markdown_links():
    text = "this is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    expected_output = [
        TextNode("this is text with a link ", "text", None),
        TextNode("to boot dev", "link", "https://www.boot.dev"),
        TextNode(" and ", "text", None),
        TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
    ]
    actual_output = extract_markdown_links(text)
    print("Actual output:", actual_output)
    print("Expected output:", expected_output)
    assert actual_output == expected_output
    print("extract_markdown_links works!")

if __name__ == "__main__":
    test_extract_markdown_images()
    test_extract_markdown_links()



