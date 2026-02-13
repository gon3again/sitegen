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
            raise ValueError()
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}>{self.value}<{self.tag}>"
        raise NotImplementedError()
        
        




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
