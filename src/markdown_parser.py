from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)
import re


def __split_or_default(old_nodes, split_node):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            split_nodes = split_node(node)
            new_nodes.extend(split_nodes)
        else:
            raise TypeError(f"{node} is not an instance of TextNode!")
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def split_delimiter(node):
        split = node.text.split(delimiter)
        nodes = []
        if len(split) == 1:
            nodes.append(node)
        elif len(split) % 2 == 0:
            raise ValueError(
                f"Invalid markdown, needs matching {delimiter} {text_type} delimiters"
            )
        else:
            is_inline = False
            for split_text in split:
                if len(split_text) > 0:
                    if is_inline:
                        nodes.append(TextNode(split_text, text_type))
                    else:
                        nodes.append(TextNode(split_text, node.text_type))
                is_inline = not is_inline
        return nodes

    return __split_or_default(old_nodes, split_delimiter)


def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    images = re.findall(regex, text)
    return images


def extract_markdown_links(text):
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    links = re.findall(regex, text)
    return links


def split_url_nodes(node, type, extract, generate_split_token):
    nodes = []
    tuples = extract(node.text)
    if len(tuples) == 0:
        nodes.append(node)
    else:
        current_text = node.text
        for tup in tuples:
            split = current_text.split(generate_split_token(tup), 1)
            split_node = TextNode(tup[0], type, tup[1])
            if split[0] != "":
                nodes.append(TextNode(split[0], node.text_type))
            nodes.append(split_node)
            current_text = split[-1]
        if len(current_text) > 0:
            nodes.append(TextNode(current_text, node.text_type))
    return nodes


def split_nodes_image(old_nodes):
    def split_images(node):
        return split_url_nodes(
            node,
            text_type_image,
            extract_markdown_images,
            lambda tup: f"![{tup[0]}]({tup[1]})",
        )

    return __split_or_default(old_nodes, split_images)


def split_nodes_link(old_nodes):
    def split_links(node):
        return split_url_nodes(
            node,
            text_type_link,
            extract_markdown_links,
            lambda tup: f"[{tup[0]}]({tup[1]})",
        )

    return __split_or_default(old_nodes, split_links)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
