from textnode import TextNode,TextType
from htmlnode import HTMLNode, LeafNode, ParentNode,text_node_to_html_node
import os
import shutil


'''
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
        
    '''



def recursive_copy_to(source:str, destination:str):

    source_folder_name = source.split("/")[-1]
    dest_folder_name = destination.split("/")[-1]
    source_exists = os.path.exists(source)
    dest_exists = os.path.exists(destination)
    if not source_exists:
        raise Exception("source does not exist")
    # del folder for clean copy
    if dest_exists:
        shutil.rmtree(destination)
    os.mkdir(destination)

    source_files = os.listdir(source)
    for i in range(len(source_files)):
        cur_source_path = os.path.join(source,source_files[i])
        cur_dest_path = os.path.join(destination,source_files[i])
        if os.path.isfile(cur_source_path):# is file
            shutil.copyfile(cur_source_path,cur_dest_path)
        else:#is dir
            if not os.path.exists(cur_dest_path):
                os.mkdir(cur_dest_path)
                recursive_copy_to(cur_source_path,cur_dest_path)# recursive call on the cur dir




    

def main():
    source = "/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/static"
    destination = "/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/public"
    recursive_copy_to(source,destination)
    





if __name__ == "__main__":
    main()
