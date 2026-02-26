from textnode import TextNode,TextType
from htmlnode import HTMLNode, LeafNode, ParentNode,text_node_to_html_node
from markdown_to_html import markdown_to_html
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


def extract_title(markdown:str):
    lines: list[str] = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:]
    raise Exception("no title found")




def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = open(from_path).read()
    title = extract_title(md)
    html = markdown_to_html(md)
    #print("_______",html,"____")
    template = open(template_path).read()
    mod_template= template.replace("{{ Title }}",title).replace("{{ Content }}", html)

    print("dest_path",dest_path)

    
    dest_file = open(dest_path,"w")
    dest_file.write(mod_template)


    #index = open(dest_path).write
    #print("template:",template)
    

    


    

def main():
    source = "/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/static"
    destination = "/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/public"
    recursive_copy_to(source,destination) # copy the contents of the static dir to the public dir


    md = open("/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/content/index.md").read()
    #print(extract_title(md))
    generate_page("/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/content/index.md","/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/template.html","/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/public/index.html")
    
    

    





if __name__ == "__main__":
    main()
