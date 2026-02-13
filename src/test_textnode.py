import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_None_url(self):
        node = TextNode("node",TextType.LINK,None)
        node2 = TextNode("node",TextType.LINK)
        self.assertEqual(node,node2)

    def test_not_eq_text(self):
        node = TextNode("this is a node",TextType.LINK,"whoisit.com")
        node2 = TextNode("this is different",TextType.LINK,"whoisit.com")
        self.assertNotEqual(node,node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC,"google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC,"ijustgothere.com")
        self.assertNotEqual(node, node2)
    
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC,"google.com")
        node2 = TextNode("This is a text node", TextType.BOLD,"google.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()