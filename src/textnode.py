from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 1 # text
    BOLD = 2 # **bold text**
    ITALIC = 3 # _italic text_
    CODE = 4 # `code text`
    LINK = 5 # [anchor text](url)
    IMAGE = 6 # ![alt text](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text # Text content
        self.text_type = text_type # TextType enum
        self.url = url # URL for link or image, if needed

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType(1):
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType(2):
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType(3):
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType(4):
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType(5):
        if not text_node.url:
            raise ValueError("Link text nodes must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType(6):
        if not text_node.url:
            raise ValueError("Image text nodes must have a URL")
        return LeafNode("img", text_node.text, {"src": text_node.url})
    else:
        raise ValueError("Unknown TextType")