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
