class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props


    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_str_list = []  # Step 1: Initialize an empty list
        
        if self.props:  # Only enter if self.props is not None
            for key, value in self.props.items():  # Step 2: Loop through key-value pairs using .items()
                props_str_list.append(f' {key}="{value}"')  # Steps 3 and 4: Format and add to list
        return ''.join(props_str_list)  # Step 5: Join list into single string

    def __repr__(self):
        return f"{self.tag} {self.value} {self.children} {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
       if value is None:
           raise ValueError("Value cannot be None")
       super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.tag:
            return self.value
        else:
            props_str = self.props_to_html()
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        if children is None or len(children) == 0:
            raise ValueError("Children is required and cannot be empty")
        super().__init__(tag=tag, children=children)


    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag must be provided")
        if self.children is None:
            raise ValueError("Children must be provided")
        if len(self.children) == 0:
            raise ValueError("Children cannot be empty")
        
        html_string = f"<{self.tag}>"
        
        for child in self.children:
            html_string += child.to_html()
            
        html_string += f"</{self.tag}>"
        return html_string
    

class ConversionError(Exception):
    pass


def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == "link":
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == "image":
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ConversionError(f"Unknown text_type: {text_node.text_type}")




if __name__ == "__main__":

    def run_tests():
        # Test nested ParentNode instances
        try:
            nested_parent = ParentNode(
                "div",
                [
                    ParentNode(
                        "section",
                        [
                            LeafNode("h1", "Header"),
                            ParentNode(
                                "article",  # Mind the typo fixed here from "artical" to "article"
                                [
                                    LeafNode("p", "Article text"),
                                    LeafNode("p", "More text"),
                                ],
                            ),
                        ],
                    ),
                    LeafNode("footer", "Footer text"),
                ]
            )
            print(nested_parent.to_html())
            print("Nested ParentNode instances passed.\n")
        except Exception as e:
            print("Nested ParentNode instances test failed:", e)

        # Test different tags and values
        try:
            print("Testing different tags and values:")
            mixed_tags = ParentNode(
                "body",
                [
                    LeafNode("h2", "Subheader"),
                    ParentNode(
                        "div",
                        [
                            LeafNode("span", "A span inside a div"),
                            LeafNode(None, "A text node without a tag"),
                        ],
                    ),
                ]
            )
            print(mixed_tags.to_html())
            print("Different tags and values test passed.\n")
        except Exception as e:
            print("Different tags and values test failed:", e)

        # Test error handling when tags or children are missing
        try:
            print("Testing error handling with missing tags:")
            parent_no_tag = ParentNode(None, [LeafNode("p", "Paragraph")])
            print(parent_no_tag.to_html())
            print("Error handling with missing tags test failed (should have raised an error).\n")
        except ValueError as e:
            print("Error handling with missing tags test passed:", e)

        try:
            print("Testing error handling with no children:")
            empty_children = ParentNode("div", [])
            print(empty_children.to_html())
            print("Error handling with no children test failed (should have raised an error).\n")
        except ValueError as e:
            print("Error handling with no children test passed:", e)

    run_tests()
