import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty(self):
        md = """
        
        
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_whitespace(self):
        md = """
        
        This is a paragraph with whitespace around it
        
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with whitespace around it"])
    
    def test_markdown_to_blocks_newlines(self):
        md = """
This is a paragraph with newlines around it


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with newlines around it"])
    
    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
This is a paragraph with multiple newlines around it



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with multiple newlines around it"])


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_header(self):
        block = "# This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADER)
    
    def test_block_to_block_type_code(self):
        block = "```\nThis is code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_to_block_type_unordered_list(self):
        block = "- This is an unordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote with **bold** text and _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text and <i>italic</i> text</blockquote></div>",
        )
    
    def test_unordered_list(self):
        md = """
- Item 1 with **bold** text
- Item 2 with _italic_ text
- Item 3 with `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1 with <b>bold</b> text</li><li>Item 2 with <i>italic</i> text</li><li>Item 3 with <code>code</code> text</li></ul></div>",
        )
    
    def test_ordered_list(self):
        md = """
1. Item 1 with **bold** text
2. Item 2 with _italic_ text
3. Item 3 with `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1 with <b>bold</b> text</li><li>Item 2 with <i>italic</i> text</li><li>Item 3 with <code>code</code> text</li></ol></div>",
        )
    
    def test_malformed_codeblock(self):
        md = """```
This is a code block without a closing tag
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)
    
    

if __name__ == "__main__":
    unittest.main()