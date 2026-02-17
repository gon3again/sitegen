from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType):
    new_nodes:list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            cur_text = old_node.text
            split_text = cur_text.split(delimiter)
            #print(f"len(split_text):{len(split_text)}, split_text:{split_text}")
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
            print("empty text node removed")
            new_nodes.remove(node)
        #print(f"new_nodes:{new_nodes}")
    return new_nodes


def split_nodes_link(old_nodes:list[TextNode]):
    result_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            split_text = node.text
            new_link_nodes = []

            for i in range(len(links)):
                new_link_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                split_text = split_text.replace("["+links[i][0]+"]"+"("+links[i][1]+")","[link]")

            split_text = split_text.split("[link]")
            new_text_nodes = []
            for t in split_text:
                
                if t != "":
                    new_text_nodes.append(TextNode(t, TextType.TEXT))

            combined_nodes = []
            combined_nodes.extend(new_text_nodes)
            combined_nodes.extend(new_link_nodes)
            
            while len(combined_nodes) > 0:
                min_index = float("inf")
                cur_node = None
                for n in combined_nodes:
                    if node.text.index(n.text) < min_index:
                        min_index = node.text.index(n.text)
                        cur_node = n
                combined_nodes.remove(cur_node)
                result_nodes.append(cur_node)
        else:
            result_nodes.append(node)     
    return result_nodes

def split_nodes_image(old_nodes:list[TextNode]):
    result_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            split_text = node.text
            new_image_nodes = []

            for i in range(len(images)):
                new_image_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                split_text = split_text.replace("!["+images[i][0]+"]"+"("+images[i][1]+")","![image]")

            split_text = split_text.split("![image]")
            new_text_nodes = []
            for t in split_text:
                
                if t != "":
                    new_text_nodes.append(TextNode(t, TextType.TEXT))

            combined_nodes = []
            combined_nodes.extend(new_text_nodes)
            combined_nodes.extend(new_image_nodes)
            
            while len(combined_nodes) > 0:
                min_index = float("inf")
                cur_node = None
                for n in combined_nodes:
                    if node.text.index(n.text) < min_index:
                        min_index = node.text.index(n.text)
                        cur_node = n
                combined_nodes.remove(cur_node)
                result_nodes.append(cur_node)
        else:
            result_nodes.append(node)
    return result_nodes


            
          


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches





# main conversion function that uses the other functions
def text_to_textnodes(text):
    cur_nodes = [TextNode(text, TextType.TEXT)]
    
    cur_nodes = split_nodes_delimiter(cur_nodes,"**",TextType.BOLD)
    #print(f"after bold check:len:{len(cur_nodes)},{cur_nodes}")
    cur_nodes = split_nodes_delimiter(cur_nodes,"_",TextType.ITALIC)
    #print(f"after italic check:len:{len(cur_nodes)},{cur_nodes}")
    cur_nodes = split_nodes_delimiter(cur_nodes,"`",TextType.CODE)
    cur_nodes = split_nodes_image(cur_nodes)
    cur_nodes = split_nodes_link(cur_nodes)
    return cur_nodes

test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
text_to_textnodes(test_text)