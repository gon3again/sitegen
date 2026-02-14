from textnode import TextNode,TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_node_to_html_node(text_node:TextNode):
    if text_node.text_type not in TextType:
        raise Exception("text_node type is not a valid type")
    match text_node.text_type:
        case TextType.TEXT.value:
            return LeafNode(None,text_node.text)
        case TextType.BOLD.value:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC.value:
            return LeafNode("i",text_node.text)
        case TextType.CODE.value:
            return LeafNode("code",text_node.text,{"href":text_node.url})
        case TextType.LINK.value:
            return LeafNode("a",text_node.text)
        case TextType.IMAGE.value:
            return LeafNode("img","",{"src":text_node.url, "alt":text_node.text})
        
    






def main():
    
    my_text_node = TextNode("this is my text", TextType.CODE.value, "google.com")
    print(my_text_node)
    text_node_to_html_node(my_text_node)





if __name__ == "__main__":
    main()
