from textnode import TextNode,TextType
from htmlnode import HTMLNode, LeafNode, ParentNode,text_node_to_html_node
from markdown_to_html import markdown_to_html
import os
import shutil
from pathlib import Path
import sys

basepath = "/"

if len(sys.argv) > 1:
    basepath = sys.argv[1]
    print("sys.argv:",sys.argv)

print("basepath:",basepath)

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




def generate_page(from_path, template_path, dest_path, basepath):
    #print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = open(from_path).read()
    title = extract_title(md)
    html = markdown_to_html(md)
    #print("_______",html,"____")
    template = open(template_path).read()
    mod_template= template.replace("{{ Title }}",title).replace("{{ Content }}", html)
    mod_template = mod_template.replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')

    dest_file = open(dest_path,"w")
    dest_file.write(mod_template)
    dest_file.close()




def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_path_content = os.path.join(".",dir_path_content)
    template_path = os.path.join(".",template_path)
    dest_dir_path = os.path.join(".",dest_dir_path)
    #print(dir_path_content,template_path,dest_dir_path)

    if not os.path.isfile(template_path):
        raise Exception("template is not a file")
    
    if os.path.isfile(dir_path_content) or os.path.isfile(dest_dir_path):
        raise Exception("dir path or dest path is a file instead of dir")
    else:
        content:list[str] = os.listdir(dir_path_content)
        destination :list[str] = os.listdir(dest_dir_path)

    md_paths:list[str] = []
    dir_to_explore:list[str] = [dir_path_content]
   

    while len(dir_to_explore) > 0:
        cur_dir = dir_to_explore.pop(0)
        dir_files:list[str] = os.listdir(cur_dir)
        #print(cur_dir+":",dir_files)
        for file in dir_files:
            cur_path = cur_dir+"/"+file
            if os.path.isfile(cur_path):
                if cur_path.endswith(".md"):
                    md_paths.append(cur_path)
            else:
                dir_to_explore.append(cur_path)

    def content_to_html_path(s:str):
        s = s.replace(dir_path_content,dest_dir_path).replace(".md",".html")
        return s
    
    html_paths:list[str] = list(map(content_to_html_path,md_paths))

    path_list = list(zip(md_paths,html_paths))

    for path_tuple in path_list:
        dest_path = Path(path_tuple[1])
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True)
        #print(path_tuple[0],template_path,path_tuple[1])
        generate_page(path_tuple[0],template_path,path_tuple[1],basepath)








    

def main():

    #copy from static folder to destination
    static_path = "/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/static"
    destination = "/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/docs"
    recursive_copy_to(static_path,destination) # copy the contents of the static dir to the public dir


    
    
    #generate_page("/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/content/index.md","/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/template.html","/home/dustin/workspace/github.com/bootdotdev/curriculum/sitegenerator/public/index.html")
    content_path = "content"
    template_path = "template.html"
    dest_path = "docs"
    generate_pages_recursive(content_path,template_path,dest_path,basepath)
    
    

    





if __name__ == "__main__":
    main()
