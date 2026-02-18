from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text" # text
    BOLD = "bold" # **bold text**
    ITALIC = "italic" # _italic text_
    CODE = "code" # `code text`
    LINK = "link" # [anchor text](url)
    IMAGE = "image" # ![alt text](url)

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
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link text nodes must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image text nodes must have a URL")
        return LeafNode("img", text_node.text, {"src": text_node.url})
    else:
        raise ValueError("Unknown TextType")