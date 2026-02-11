from textnode import *

def main():
    node = TextNode("This is some anchor text", "link", 'https://www.boot.dev')
    print(node.__repr__())

main()