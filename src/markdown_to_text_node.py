from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type_input:TextType):
    result:list[TextNode] = []
    for cur_node in old_nodes:
        #print(f"curnode:__{cur_node}")
        #print(f"cur_type:__{cur_node.text_type}")
        if cur_node.text_type == TextType.TEXT:
            split_text = cur_node.text.split(delimiter,2)
            match len(split_text):
                case 3:# delimiter found
                    n1 = TextNode(split_text[0],TextType.TEXT)
                    n2 = TextNode(split_text[1],text_type_input)
                    n3 = TextNode(split_text[2],TextType.TEXT)
                    result.append(n1)
                    result.append(n2)
                    if delimiter in split_text[2]:
                        result.extend(split_nodes_delimiter([n3], delimiter, text_type_input))
                    else:
                        result.append(n3)
                case 2:# only 1 delimiter found
                    raise Exception(f"invalid Markdown syntax: only 1 delimiter:{delimiter} found")
                case 1:# no delimiter, no changes
                    result.append(cur_node)
                case _:
                    raise Exception("invalid Markdown syntax")
        else:
            result.append(cur_node)

    for n in result:
        if n.text_type == TextType.TEXT and n.text == "":
            result.remove(n)
    return result




def split_nodes_link(old_nodes:list[TextNode]):
    result_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            split_text:str = node.text
            
            while len(links) > 0:
                cur_link_index = split_text.index(links[0][0])
                if cur_link_index != 1:# link not at start make new text_node
                    text_node = TextNode(split_text[0:cur_link_index-1],TextType.TEXT)
                    result_nodes.append(text_node)
                    split_text = split_text[cur_link_index-1:]
                else:# link at start
                    link_node = TextNode(links[0][0],TextType.LINK,links[0][1])
                    result_nodes.append(link_node)
                    split_text = split_text.replace("["+links[0][0]+"]","").replace("("+links[0][1]+")","")
                    links.pop(0)

            if len(split_text) > 0: #if there is text left after the links have been handled-> add the rest of the text
                text_node = TextNode(split_text,TextType.TEXT)
                result_nodes.append(text_node)
        else:# node is not Texttype.TEXT (dont change it)
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
#text_to_textnodes(test_text)





t2 = "**this** is an example of multiple **bold** words. Also a [wiki](https://en.wikipedia.org/wiki/Art)"
input_node = TextNode(t2, TextType.TEXT)
#print(f"result={split_nodes_delimiter([input_node], "**", TextType.BOLD)}")