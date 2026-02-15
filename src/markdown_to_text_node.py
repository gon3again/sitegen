from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType):
    new_nodes:list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            cur_text = old_node.text
            split_text = cur_text.split(delimiter)
            print(f"len(split_text):{len(split_text)}, split_text:{split_text}")
            match len(split_text):
                case 3:# delimiter found
                    n1 = TextNode(split_text[0], TextType.TEXT)
                    n2 = TextNode(split_text[1], text_type)
                    n3 = TextNode(split_text[2], TextType.TEXT)
                    new_nodes.extend([n1, n2, n3])
                case 2:# only 1 delimiter found
                    raise Exception("invalid Markdown syntax: only 1 delimiter found")
                case 1:# no delimiter, no changes
                    new_nodes.append(old_node)
                case _:
                    raise Exception("invalid Markdown syntax")
                
        for node in new_nodes:
            if node.text == "":
                new_nodes.remove(node)
        print(f"new_nodes:{new_nodes}")
        return new_nodes


