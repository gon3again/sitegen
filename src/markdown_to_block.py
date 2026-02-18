from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def block_to_block_type(block:str):
    lines = block.split("\n")
    
    #ordered list
    for i in range(len(lines)):
        if lines[i].startswith(f"{i+1}. "):
            if i == len(lines)-1:
                return BlockType.ORDERED_LIST
        else:
            break
    #unordered list
    for i in range(len(lines)):
        if lines[i].startswith(f"- "):
            if i == len(lines)-1:
                return BlockType.UNORDERED_LIST
        else:
            break
    ##quote
    for i in range(len(lines)):
        if lines[i].startswith(f">"):
            if i == len(lines)-1:
                return BlockType.QUOTE
        else:
            break
            

    
    if re.match(r"^#{1,6}( )", block):
        return BlockType.HEADING
    #``` code ```
    elif re.match(r"^`{3}\n[^`]+`{3}$",block):
        return BlockType.CODE
   
    return BlockType.PARAGRAPH









def markdown_to_blocks(markdown:str):
    block_strings:list[str] = []
    block_strings = markdown.split("\n\n")
    block_strings = list(map(str.strip,block_strings))
    for block in block_strings:
        if block == "":
            block_strings.remove(block)
    return block_strings
    

