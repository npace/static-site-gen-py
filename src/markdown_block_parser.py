block_type_paragraph = "paragraph"
block_type_heading_1 = "heading 1"
block_type_heading_2 = "heading 2"
block_type_heading_3 = "heading 3"
block_type_heading_4 = "heading 4"
block_type_heading_5 = "heading 5"
block_type_heading_6 = "heading 6"
block_type_code = "code"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"
block_type_quote = "quote"


def text_to_blocks(text):
    blocks = text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    if block.startswith("# "):
        return block_type_heading_1
    elif block.startswith("## "):
        return block_type_heading_2
    elif block.startswith("### "):
        return block_type_heading_3
    elif block.startswith("#### "):
        return block_type_heading_4
    elif block.startswith("##### "):
        return block_type_heading_5
    elif block.startswith("###### "):
        return block_type_heading_6
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    else:
        lines = block.split("\n")
        if is_valid_unordered_list(lines):
            return block_type_unordered_list
        elif is_valid_ordered_list(lines):
            return block_type_ordered_list
        elif is_valid_quote(lines):
            return block_type_quote
    return block_type_paragraph


def is_valid_unordered_list(lines):
    for line in lines:
        line = line.strip()
        if not (line.startswith("* ") or line.startswith("- ")):
            return False
    return True


def is_valid_ordered_list(lines):
    order = 1
    for line in lines:
        line = line.strip()
        if not line.startswith(f"{order}. "):
            return False
        else:
            order += 1
    return True


def is_valid_quote(lines):
    for line in lines:
        line = line.strip()
        if not line.startswith(">"):
            return False
    return True
