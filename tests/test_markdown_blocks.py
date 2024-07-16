import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from htmlnode import LeafNode
from markdown_blocks import (
    markdown_to_block, 
    block_to_block_type,
    markdown_to_html_node,
    heading_to_html_node,
    paragraph_to_html_node,
    code_to_html_node,
    olist_to_html_node,
    ulist_to_html_node,
    quote_to_html_node

) 

class TestMarkdownBlocks(unittest.TestCase):
    
    def test_markdown_to_block(self):
        example_markdown = """
# Heading 1

A paragraph of text.

> A quote of text.

```code block```

- An unordered list item

Another paragraph here.

1. An ordered list item
"""

        expected_blocks = [
            "# Heading 1",
            "A paragraph of text.",
            "> A quote of text.",
            "```code block```",
            "- An unordered list item",
            "Another paragraph here.",
            "1. An ordered list item"
        ]

        self.assertEqual(markdown_to_block(example_markdown), expected_blocks)


    def test_markdown_to_block_edge_cases(self):
        # Empty input
        empty_input = ""
        self.assertEqual(markdown_to_block(empty_input), [])

        # Mixed newlines
        mixed_newlines_input = "\n\n\n\n# Heading 1\n\n\n\nA paragraph of text.\n\n\n\n"
        expected_mixed_blocks = ["# Heading 1", "A paragraph of text."]
        self.assertEqual(markdown_to_block(mixed_newlines_input), expected_mixed_blocks)

        # Single line input
        single_line_input = "# Heading 1"
        expected_single_line = ["# Heading 1"]
        self.assertEqual(markdown_to_block(single_line_input), expected_single_line)

        # Multiple paragraphs without double newline
        multiple_paragraphs_input = "Paragraph one.\nParagraph two."
        expected_multiple_paragraphs = ["Paragraph one.\nParagraph two."]
        self.assertEqual(markdown_to_block(multiple_paragraphs_input), expected_multiple_paragraphs)


    def test_block_to_block_type(self):
        test_cases = [
            ("# Heading 1", "heading"),
            ("A paragraph of text.", "paragraph"),
            ("> A quoted text.", "quote"),
            ("```code block```", "code"),
            ("- An unordered list item", "unordered list"),
            ("1. An ordered list item", "ordered list")
        ]
        
        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)
    
    def test_block_to_block_type_edge_cases(self):
        edge_cases = [
            ("#Heading without space", "paragraph"),
            ("-No space after dash", "paragraph"),
            ("1.Not a space after number", "paragraph"),
            ("```\ncode block", "paragraph")
        ]
        
        for block, expected in edge_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)


class TestMarkdownToHTMLFunctions(unittest.TestCase):

    def test_markdown_to_html_node(self):
        example_markdown = """
# Heading 1

A paragraph of text.

> A quote of text.

```code block```

- An unordered list item

1. An ordered list item
"""
        expected_html = (
            "<h1>Heading 1</h1>"
            "<p>A paragraph of text.</p>"
            "<blockquote><p>A quote of text.</p></blockquote>"
            "<pre><code>code block</code></pre>"
            "<ul><li>An unordered list item</li></ul>"
            "<ol><li>An ordered list item</li></ol>"
        )

        html_result = markdown_to_html_node(example_markdown)
        self.assertEqual(html_result, expected_html)

    def test_paragraph_to_html_node(self):
        block = "A paragraph of text."
        node = paragraph_to_html_node(block)
        self.assertEqual(node.tag, "p")
        self.assertEqual(len(node.children), 1)
        self.assertIsInstance(node.children[0], LeafNode)
        self.assertEqual(node.children[0].value, "A paragraph of text.")

    def test_code_to_html_node(self):
        block = "```code block```"
        node = code_to_html_node(block)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "code")
        self.assertEqual(len(node.children[0].children), 1)
        self.assertIsInstance(node.children[0].children[0], LeafNode)
        self.assertEqual(node.children[0].children[0].value, "code block")

    def test_olist_to_html_node(self):
        block = "1. An ordered list item\n2. Another ordered list item"
        node = olist_to_html_node(block)

        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 2)
    
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(len(node.children[0].children), 1)
        self.assertIsInstance(node.children[0].children[0], LeafNode)
        self.assertEqual(node.children[0].children[0].value, "An ordered list item")
    
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(len(node.children[1].children), 1)
        self.assertIsInstance(node.children[1].children[0], LeafNode)
        self.assertEqual(node.children[1].children[0].value, "Another ordered list item")

    def test_ulist_to_html_node(self):
        block = "- An unordered list item\n- Another unordered list item"
        node = ulist_to_html_node(block)

        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 2)
    
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(len(node.children[0].children), 1)
        self.assertIsInstance(node.children[0].children[0], LeafNode)
        self.assertEqual(node.children[0].children[0].value, "An unordered list item")
    
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(len(node.children[1].children), 1)
        self.assertIsInstance(node.children[1].children[0], LeafNode)
        self.assertEqual(node.children[1].children[0].value, "Another unordered list item")


    def test_quote_to_html_node(self):
        block = "> A quote of text.\n> Another line of the quote."
        node = quote_to_html_node(block)

        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(len(node.children), 2)  # Each line is a different paragraph
    
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(len(node.children[0].children), 1)
        self.assertIsInstance(node.children[0].children[0], LeafNode)
        self.assertEqual(node.children[0].children[0].value, "A quote of text.")
    
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(len(node.children[1].children), 1)
        self.assertIsInstance(node.children[1].children[0], LeafNode)
        self.assertEqual(node.children[1].children[0].value, "Another line of the quote.")

    


if __name__ == "__main__":
    unittest.main()

    