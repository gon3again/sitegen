from markdown_to_block import BlockType,markdown_to_blocks,block_to_block_type
from markdown_to_text_node import text_to_textnodes
from textnode import TextNode,TextType
from htmlnode import HTMLNode,LeafNode,ParentNode,text_node_to_html_node




def markdown_to_html(markdown:str):
    blocks:list[str] = markdown_to_blocks(markdown)
    block_types:list[BlockType] = []
    block_html_nodes:list[HTMLNode] = []

    for block in blocks:
        cur_block_type:BlockType = block_to_block_type(block)
        cur_block_tag = block_type_to_tag(cur_block_type,block)
        block = fix_block_format(block,cur_block_type,cur_block_tag)
        
        block_html_node = ParentNode(cur_block_tag,text_to_children(block, cur_block_tag))
        if cur_block_tag == "code":
            pre_node = ParentNode("pre",[block_html_node])
            block_html_nodes.append(pre_node)
        else:
            block_html_nodes.append(block_html_node)
    root_div_html_node = ParentNode("div", block_html_nodes)
    #print(root_div_html_node)
    return root_div_html_node.to_html()







def text_to_children(text:str, cur_block_tag:str):
    text_nodes = ""
    if cur_block_tag == "code":
        text_nodes = [TextNode(text,TextType.TEXT)]
    else:
        text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node,text_nodes))
    
    return html_nodes
  
def fix_block_format(block:str,block_type:BlockType,tag:str):
    lines = block.split("\n")
    if tag!= "code":
        block = block.replace("\n"," ")
    match block_type:
        case BlockType.PARAGRAPH:
            return block
        case BlockType.HEADING:
            index = int(tag[1])
            block = block[index+1:]
        case BlockType.CODE:
            block = block.replace("```","")
            if block.startswith("\n"): 
                block = block[1:]
        case BlockType.QUOTE:
            for i in range(len(lines)):
                if lines[i].startswith("> "):
                    lines[i] = lines[i][2:]
                else:
                    lines[i] = lines[i][1:]
            block = "\n".join(lines)
        case BlockType.UNORDERED_LIST:
            for i in range(len(lines)):
                lines[i] = "<li>"+lines[i][2:]+"</li>"
                #print("lines[i]:",lines[i])
            block = "".join(lines)

        case BlockType.ORDERED_LIST:
            for i in range(len(lines)):
                lines[i] = "<li>"+lines[i][3:]+"</li>"
            block = "".join(lines)
    return block


def block_type_to_tag(block_type:BlockType, block):

    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            for i in range(7):
                if block[i] != "#":
                    return f"h{i}"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"#li
        case BlockType.ORDERED_LIST:
            return "ol"#li



md = """- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)"""
    
#result ="<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"


#print(markdown_to_html(md))