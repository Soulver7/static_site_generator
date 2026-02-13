import re

from textnode import TextNode, TextType



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("Invalid Markdown syntax: Closing delimiter missing")
            else:
                node_cluster = []
                for i in range(len(parts)):
                    if parts[i] == "":
                        continue
                    if i % 2 == 0:
                        node_cluster.append(TextNode(parts[i], TextType.TEXT))
                    else:
                        node_cluster.append(TextNode(parts[i], text_type))
                new_nodes.extend(node_cluster)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)


def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                current_text = node.text
                for alt_text, url in matches:
                    parts = current_text.split(f'![{alt_text}]({url})', 1)
                    if len(parts) != 2:
                        raise ValueError("Invalid Markdown syntax: Image not closed properly")
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                    current_text = parts[1]
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_links(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                current_text = node.text
                for alt_text, url in matches:
                    parts = current_text.split(f'[{alt_text}]({url})', 1)
                    if len(parts) != 2:
                        raise ValueError("Invalid Markdown syntax: Link not closed properly")
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                    current_text = parts[1]
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes