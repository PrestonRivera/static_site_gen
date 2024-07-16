import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        # Create an HTMLNode instance with props
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        # Call the props_to_html method
        result = node.props_to_html()
        # Expected output
        expected = ' href="https://www.google.com" target="_blank"'
        # Assert the result matches the expected output
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()