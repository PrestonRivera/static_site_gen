import unittest
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from main import generate_page

class TestGeneratePage(unittest.TestCase):

    def setUp(self):
        os.makedirs("tests", exist_ok=True)

        # Creating temporary markdown and template files for testing purposes
        self.markdown_path = "tests/test_content.md"
        self.template_path = "tests/test_template.html"
        self.output_path = "tests/test_output.html"

        with open(self.markdown_path, "w") as f:
            f.write("# Test Title\nThis is a test content.")

        with open(self.template_path, "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

    def tearDown(self):
        # Clean up the files after the test
        try:
            os.remove(self.markdown_path)
            os.remove(self.template_path)
            os.remove(self.output_path)
        except OSError:
            pass

    @patch('utils.extract_titles', return_value="Test Title")
    @patch('main.markdown_to_html_node')
    def test_generate_page_creates_file(self, mock_md_to_html, mock_extract_titles):
        # Mock the return value of markdown_to_html_node
        mock_md_to_html.return_value.to_html.return_value = "<p>This is a test content.</p>"

        # Test if the function generates the output file
        generate_page(self.markdown_path, self.template_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

    @patch('utils.extract_titles', return_value="Test Title")
    @patch('main.markdown_to_html_node')
    def test_generate_page_content(self, mock_md_to_html, mock_extract_titles):
        # Mock the return value of markdown_to_html_node
        mock_md_to_html.return_value.to_html.return_value = "<p>This is a test content.</p>"

        # Call the function to generate the page
        generate_page(self.markdown_path, self.template_path, self.output_path)

        # Read the content of the generated file
        with open(self.output_path, "r") as f:
            generated_content = f.read()

        # Check if the title placeholder is correctly replaced
        self.assertIn("<title>Test Title</title>", generated_content)
        # Check if the content placeholder is correctly replaced
        self.assertIn("<body><p>This is a test content.</p></body>", generated_content)
       


if __name__ == "__main__":
    unittest.main()