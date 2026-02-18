import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode,LeafNode,ParentNode,text_node_to_html_node
from markdown_to_text_node import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link,split_nodes_image, text_to_textnodes



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



    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        #print(html_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")



    #markdown_to_text_node tests:

    def test_markdown_to_text_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ])
        
    def test_markdown_to_text_node_no_delimiter(self):
        node = TextNode("There is no delimiter here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], node)
    
    def test_markdown_to_text_node_Bold(self):
        node = TextNode("**Bold text** is important", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
    [
        TextNode("Bold text", TextType.BOLD),
        TextNode(" is important", TextType.TEXT),
    ])
    
    def test_markdown_to_text_node_italic(self):
        node = TextNode("Italicized text is the *cat's meow*.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, 
    [
        TextNode("Italicized text is the ", TextType.TEXT),
        TextNode("cat's meow", TextType.ITALIC),
        TextNode(".", TextType.TEXT)
    ])
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_nodes_link(self):
        t1 = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT)

        t2 = TextNode(
        "[to google](https://www.google.com) and [wiki](https://de.wikipedia.org) here is more text",
        TextType.TEXT)

        #print(f"this should return [nodes]:{split_nodes_link([test_node])}")

        self.assertEqual(split_nodes_link([t1]),
        [TextNode("This is text with a link ",TextType.TEXT,None),
         TextNode("to boot dev",TextType.LINK,"https://www.boot.dev"),
         TextNode(" and ",TextType.TEXT,None),
         TextNode("to youtube",TextType.LINK,"https://www.youtube.com/@bootdotdev")])
        
        self.assertEqual(split_nodes_link([t2]),
        [TextNode("to google",TextType.LINK,"https://www.google.com"),
         TextNode(" and ",TextType.TEXT,None),
         TextNode("wiki",TextType.LINK,"https://de.wikipedia.org"),
         TextNode(" here is more text",TextType.TEXT,None),
         ])
        
        self.assertEqual(split_nodes_link([t1,t2]),
        [TextNode("This is text with a link ",TextType.TEXT,None),
         TextNode("to boot dev",TextType.LINK,"https://www.boot.dev"),
         TextNode(" and ",TextType.TEXT,None),
         TextNode("to youtube",TextType.LINK,"https://www.youtube.com/@bootdotdev"),

         TextNode("to google",TextType.LINK,"https://www.google.com"),
         TextNode(" and ",TextType.TEXT,None),
         TextNode("wiki",TextType.LINK,"https://de.wikipedia.org"),
         TextNode(" here is more text",TextType.TEXT,None),
         ])
        
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        t1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(t1),
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

        #TO DO: multiple of the same delimiter is not implemented yet.
        t2 = "**this** is an example of multiple **bold** words. Also a [wiki](https://en.wikipedia.org/wiki/Art)"
        self.assertEqual(text_to_textnodes(t2),[
            TextNode("this", TextType.BOLD),
            TextNode(" is an example of multiple ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words. Also a ", TextType.TEXT),
            TextNode("wiki", TextType.LINK,"https://en.wikipedia.org/wiki/Art"),
        ])
        
if __name__ == "__main__":
    unittest.main()