import unittest
from image_link_splitter import split_nodes_images, split_nodes_links
from textnode import TextNode


class TestImageLinkSplitter(unittest.TestCase):

    def test_split_node_images(self):
        node = TextNode("This is text with an image ![example](http://example.com) and more text", "text")
        new_nodes = split_nodes_images([node])
        expected_nodes = [
            TextNode("This is text with an image ", "text"),
            TextNode("example", "image", "http://example.com"),
            TextNode(" and more text", "text")
        ]

        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes} but got {new_nodes}")

    def test_split_nodes_links(self):
        node = TextNode("Text with a [link](http://example.com).", "text")
        new_nodes = split_nodes_links([node])
        expected_nodes = [
            TextNode("Text with a ", "text"),
            TextNode("link", "link", "http://example.com"),
            TextNode(".", "text")
        ]

        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes} but got {new_nodes}")

    def test_no_links_images(self):
        node = TextNode("Just some plain text without links or images.", "text")
        new_nodes_image = split_nodes_images([node])
        new_nodes_link = split_nodes_links([node])
        expected_nodes = [node]

        self.assertEqual(new_nodes_image, expected_nodes, f"Expected {expected_nodes} but got {new_nodes_image}")
        self.assertEqual(new_nodes_link, expected_nodes, f"Expected {expected_nodes} but got {new_nodes_link}")

    def test_multiple_links(self):
        node = TextNode("Text with multiple [links](http://link1.com) and another [link](http://link2.com).", "text")
        new_nodes = split_nodes_links([node])
        expected_nodes = [
            TextNode("Text with multiple ", "text"),
            TextNode("links", "link", "http://link1.com"),
            TextNode(" and another ", "text"),
            TextNode("link", "link", "http://link2.com"),
            TextNode(".", "text")
        ]

        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes} but got {new_nodes}")

    def test_multiple_images(self):
        node = TextNode("Text with multiple images ![img1](http://img1.com) and ![img2](http://img2.com).", "text")
        new_nodes = split_nodes_images([node])
        expected_nodes = [
            TextNode("Text with multiple images ", "text"),
            TextNode("img1", "image", "http://img1.com"),
            TextNode(" and ", "text"),
            TextNode("img2", "image", "http://img2.com"),
            TextNode(".", "text")
        ]

        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes} but got {new_nodes}")

    def test_mixed_content(self):
        node = TextNode("Mixed content with a [link](http://link.com) and an image ![img](http://img.com).", "text")
        nodes_after_image_split = split_nodes_images([node])
        
        expected_after_image_split = [
            TextNode("Mixed content with a [link](http://link.com) and an image ", "text"),
            TextNode("img", "image", "http://img.com"),
            TextNode(".", "text")
        ]

        self.assertEqual(nodes_after_image_split, expected_after_image_split, f"Expected {expected_after_image_split} but got {nodes_after_image_split}")

        final_nodes_after_link_split = split_nodes_links(nodes_after_image_split)
        
        expected_final_nodes = [
            TextNode("Mixed content with a ", "text"),
            TextNode("link", "link", "http://link.com"),
            TextNode(" and an image ", "text"),
            TextNode("img", "image", "http://img.com"),
            TextNode(".", "text")
        ]

        self.assertEqual(final_nodes_after_link_split, expected_final_nodes, f"Expected {expected_final_nodes} but got {final_nodes_after_link_split}")

    def test_empty_text(self):
        node = TextNode("", "text")
        new_nodes_image = split_nodes_images([node])
        new_nodes_link = split_nodes_links([node])
        expected_nodes = [node]

        self.assertEqual(new_nodes_image, expected_nodes, f"Expected {expected_nodes} but got {new_nodes_image}")
        self.assertEqual(new_nodes_link, expected_nodes, f"Expected {expected_nodes} but got {new_nodes_link}")

    def test_malformed_image_syntax(self):
        node = TextNode("Malformed image syntax ![img(http://img.com).", "text")
        new_nodes = split_nodes_images([node])
        expected_nodes = [node]  # Expect it to be unchanged

        self.assertEqual(new_nodes, expected_nodes, f"Expected {expected_nodes} but got {new_nodes}")


if __name__ == '__main__':
    unittest.main()