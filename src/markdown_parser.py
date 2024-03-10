from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            split = node.text.split(delimiter)
            if len(split) == 1:
                new_nodes.append(node)
            else:
                is_inline = False
                for split_text in split:
                    if len(split_text) > 0:
                        if is_inline:
                            new_nodes.append(TextNode(split_text, text_type))
                        else:
                            new_nodes.append(TextNode(split_text, node.text_type))
                    is_inline = not is_inline
        else:
            new_nodes.append(node)
    return new_nodes
