import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "This is test text", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "This is test text", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_props_to_html2(self):
        node = HTMLNode("p", "This is test text", None, {"test": "This is a test"})
        node2 = HTMLNode("p", "This is test text", None, {"test": "This is a test"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_props_to_html3(self):
        node = HTMLNode("p", "This is test text", None, {"hrumph": "https://www.boot.dev", "Target": "_blank"})
        node2 = HTMLNode("p", "This is test text", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

    def test_props_to_html4(self):
        node = HTMLNode("p", "This is test text", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "This is test text", None, {"target": "_blank"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

    def test_props_to_html5(self):
        node = HTMLNode("p", "This is test text", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "This is test text", None, {"href": "www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "bold")
        self.assertEqual(f'This is a {node.to_html()} word.', 'This is a <b>bold</b> word.')

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "italic")
        self.assertEqual(f'This is an {node.to_html()} word.', 'This is an <i>italic</i> word.')
    
    def test_leaf_to_html_code(self):
        node = LeafNode("code", "This is code")
        self.assertEqual(node.to_html(), "<code>This is code</code>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link", {"href": "https://www.test.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.test.com">link</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "alt text", {"src": "https://www.test.com/image.png"})
        self.assertEqual(node.to_html(), '<img src="https://www.test.com/image.png">alt text</img>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("spam", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><spam>child2</spam></div>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )
    
    def test_to_html_with_nested_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"style": "color: red;"})
        child_node = ParentNode("span", [grandchild_node], {"class": "child"})
        parent_node = ParentNode("div", [child_node], {"id": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent"><span class="child"><b style="color: red;">grandchild</b></span></div>',
        )
    
    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()