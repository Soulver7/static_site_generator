from enum import Enum
import re

from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADER = "header"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            result.append(stripped)
    return result


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADER
    elif block.startswith("```") and block.endswith("\n```") and len(lines) > 1:
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        lines = block.split("\n")

        if block_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            children = text_to_children(text)
            nodes.append(ParentNode("p", children))

        elif block_type == BlockType.HEADER:
            hashes = 0
            for char in block:
                if char == "#":
                    hashes += 1
                else:
                    break
            if hashes + 1 >= 1:
                raise ValueError("Invalid header syntax: Too many # characters")
            children = text_to_children(block[hashes+1:])
            nodes.append(ParentNode(f'h{hashes}', children))

        elif block_type == BlockType.CODE:
            node = TextNode(block[4:-3], TextType.TEXT)
            child = text_node_to_html_node(node)
            code = ParentNode("code", [child])
            nodes.append(ParentNode("pre", [code]))

        elif block_type == BlockType.QUOTE:
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("Invalid quote syntax: Each line must start with '>'")
                else:
                    new_lines.append(line.lstrip(">").strip())
            text_value = " ".join(new_lines)
            children = text_to_children(text_value)
            nodes.append(ParentNode("blockquote", children))

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []
            for item in lines:
                if not item.startswith("- "):
                    raise ValueError("Invalid unordered list syntax: Each line must start with '- '")
                else:
                    child = text_to_children(item[2:])
                    list_items.append(ParentNode("li", child))
            nodes.append(ParentNode("ul", list_items))

        elif block_type == BlockType.ORDERED_LIST:
            list_items = []
            for item in lines:
                sections = item.split(". ", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid ordered list syntax: Each line must start with a number followed by '.'")
                else:
                    child = text_to_children(sections[1])
                    list_items.append(ParentNode("li", child))
            nodes.append(ParentNode("ol", list_items))
        
        else:
            raise ValueError("Unknown block type")
        
    return ParentNode("div", nodes)
    