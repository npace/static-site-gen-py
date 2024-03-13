from markdown_block_parser import (
    block_type_paragraph,
    block_type_heading_1,
    block_type_heading_2,
    block_type_heading_3,
    block_type_heading_4,
    block_type_heading_5,
    block_type_heading_6,
    block_type_code,
    block_type_unordered_list,
    block_type_ordered_list,
    block_type_quote,
    text_to_blocks,
    block_to_block_type,
)
from markdown_parser import text_to_textnodes
from htmlnode import LeafNode, ParentNode, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = text_to_blocks(markdown)
    block_htmls = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_htmls.append(block_to_html_node(block, block_type))
    return ParentNode("div", block_htmls)


def block_to_html_node(block, block_type):
    if block_type == block_type_paragraph:
        leaf_nodes = __block_to_nodes(block)
        return ParentNode("p", leaf_nodes)
    elif block_type in __header_types_dict:
        text_nodes = __removed_prefix_block_to_nodes(block, "# ")
        leaf_nodes = __text_nodes_to_html(text_nodes)
        return ParentNode(__header_types_dict[block_type], leaf_nodes)
    elif block_type == block_type_unordered_list:
        leaf_nodes = __block_to_list_item_nodes(block)
        return ParentNode("ul", leaf_nodes)
    elif block_type == block_type_ordered_list:
        leaf_nodes = __block_to_list_item_nodes(block)
        return ParentNode("ol", leaf_nodes)
    elif block_type == block_type_quote:
        text_nodes = __quote_block_to_nodes(block)
        leaf_nodes = __text_nodes_to_html(text_nodes)
        paragraph = ParentNode("p", leaf_nodes)
        return ParentNode("blockquote", [paragraph])
    elif block_type == block_type_code:
        return ParentNode("pre", __block_to_nodes(block))


def __removed_prefix_block_to_nodes(block, prefix):
    text_nodes = []
    split = block.split("\n")
    line_count = len(split)
    for i in range(0, line_count):
        line = split[i]
        split_line = line.split(prefix, 1)
        text = split_line[1]
        text_nodes.extend(text_to_textnodes(text))
    return text_nodes


def __quote_block_to_nodes(block):
    text_nodes = []
    lines = block.split("\n")
    line_count = len(lines)
    for i in range(0, line_count):
        line = lines[i]
        if line.startswith("> "):
            text = line.removeprefix("> ")
        else:
            text = line.removeprefix(">")
        if i < (line_count - 1):
            text += "\n"
        text_nodes.extend(text_to_textnodes(text))
    return text_nodes


def __block_to_nodes(block):
    text_nodes = text_to_textnodes(block)
    return __text_nodes_to_html(text_nodes)


def __text_nodes_to_html(text_nodes):
    return list(map(lambda n: text_node_to_html_node(n), text_nodes))


def __block_to_list_item_nodes(block):
    text_nodes = __removed_prefix_block_to_nodes(block, " ")
    return list(
        map(lambda n: ParentNode("li", [text_node_to_html_node(n)]), text_nodes)
    )


__header_types_dict = {
    block_type_heading_1: "h1",
    block_type_heading_2: "h2",
    block_type_heading_3: "h3",
    block_type_heading_4: "h4",
    block_type_heading_5: "h5",
    block_type_heading_6: "h6",
}
