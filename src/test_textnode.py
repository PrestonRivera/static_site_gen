import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_text_type_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node too", "italic")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", "bold", url=None)
        node2 = TextNode("This is a text node", "bold", url="http://example.com")
        self.assertNotEqual(node, node2)

    def test_text_none(self):
        node = TextNode(None, "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_type_none(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", None)
        self.assertNotEqual(node, node2)

    def test_url_text_none(self):
        node = TextNode("This is a text node", "bold", url="http://example.com")
        node2 = TextNode(None, "bold", url=None)
        self.assertNotEqual(node, node2)

    def test_all_none(self):
        node = TextNode("This is a text node", "bold", url="http://example.com")
        node2 = TextNode(None, None, None)
        self.assertNotEqual(node, node2)

    def test_different_text_types(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node", "underline")
        self.assertNotEqual(node, node3)

    def test_dif_text_types_same_text_url(self):
        node = TextNode("This is a text node", "bold", url="http://example.com")
        node2 = TextNode("This is a text node", "italic", url="http://example.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_all_properties(self):
        node = TextNode("This is a text node", "bold", url="http://example.com")
        node2 = TextNode("This is a text node", "bold", url="http://example.com")
        self.assertEqual(node, node2)




if __name__ == "__main__":
    unittest.main()

