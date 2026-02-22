from markdown_to_block import BlockType,markdown_to_blocks,block_to_block_type
from markdown_to_text_node import text_to_textnodes
from textnode import TextNode,TextType
from htmlnode import HTMLNode,LeafNode,ParentNode,text_node_to_html_node


def markdown_to_html(markdown:str):
    blocks:list[str] = markdown_to_blocks(markdown)
    block_types:list[BlockType] = []
    html_nodes:list[HTMLNode] = []
    for block in blocks:
        cur_block_type:BlockType = block_to_block_type(block)
        cur_block_tag = block_type_to_tag(cur_block_type,block)
        # new mod_markdown_block
        block = mod_markdown_block(block, cur_block_type, cur_block_tag)
        # to do:(leafnode) children of html nodes are not set currently
        cur_html_node = LeafNode(cur_block_tag,block)
        html_nodes.append(cur_html_node)
    for html_node in html_nodes:
        html_node.value = mod_inner_text(html_node)

    result_text:str =""
    for html_node in html_nodes:
        cur_val:str = html_node.value
        if html_node.tag!= "code":
            cur_val = cur_val.replace("\n"," ")
    
        result_text += f"<{html_node.tag}>"+cur_val+f"</{html_node.tag}>"
        if html_node.tag == "code":
            result_text = "<pre>" + result_text + "</pre>"

    result_text = f"<div>" + result_text + f"</div>"
    return result_text
        

    

def mod_inner_text(html_node:HTMLNode):
    if html_node.tag == "code":
        #print(f"html_node.value________:{html_node.value}")
        return html_node.value
    text = html_node.value

    text_nodes = text_to_textnodes(text)
    new_html_nodes = list(map(text_node_to_html_node,text_nodes))
    result_text = ""
    for new_html_node in new_html_nodes:
        result_text += new_html_node.to_html()  
    return result_text

# adds tags for blocks and list elements while removing markdown identifiers.
def mod_markdown_block(block:str,block_type:BlockType,tag:str):
    #print(f"block:{block},tag:{tag}")
    lines = block.split("\n")
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














'''print(text_to_textnodes("""1. hello,
2. who
3. is
4. waldo?"""))'''











md_test1 = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

##test
test_markdown = """## Waldo

1. hello,
2. who
3. is
4. waldo?

a normal paragraph

> quote text is here

- Coffee
- Milk
- Tea

```
a = "Hello, World!"
print(a.lower())
```"""



md_code = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""


#markdown_to_html_node(test_markdown)
print(markdown_to_html(md_code))
