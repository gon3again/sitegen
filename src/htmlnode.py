from textnode import TextNode,TextType

def text_node_to_html_node(text_node:TextNode):
        if text_node.text_type not in TextType:
            raise Exception("text_node type is not a valid type")
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None,text_node.text)
            case TextType.BOLD:
                return LeafNode("b",text_node.text)
            case TextType.ITALIC:
                return LeafNode("i",text_node.text)
            case TextType.CODE:
                return LeafNode("code",text_node.text,{"href":text_node.url})
            case TextType.LINK:
                return LeafNode("a",text_node.text)
            case TextType.IMAGE:
                return LeafNode("img","",{"src":text_node.url, "alt":text_node.text})

class HTMLNode:
    def __init__(self, tag:str=None, value:str=None, children:list["HTMLNode"]=None, props:dict[str,str]=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        result = ""
        for prop in self.props:
            self.props[prop]
            result += " "+prop+"="+ self.props[prop]
        return result
    

    

    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag:str, value:str, props:dict[str,str]=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == "":
            if self.tag == "img":
                #return f"<img src={self.props["src"]} alt={self.props["alt"]}"
                return f"<img{self.props_to_html()}>"
                print(self.tag,self.props)
            else:
                raise ValueError()
        if self.tag == None:
            return self.value
        else:
            
            return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list["HTMLNode"], props:dict[str,str]=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("tag is None")
        if self.children == None:
            raise ValueError("children == None")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}>{children_html}</{self.tag}>"
        
        


node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

#print(node.to_html())



'''
test_props = {
    "href": "https://www.google.com",
    "target": "_blank",
}

my_html_node = HTMLNode(props=test_props)
print(my_html_node.props_to_html())
print(my_html_node)



test_props = {
    "href": "https://www.google.com",
    "target": "_blank",
}

my_html_leaf_node = LeafNode(tag="p",value="this is the value", props=test_props)
print(my_html_leaf_node.to_html())
'''