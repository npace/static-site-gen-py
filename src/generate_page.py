from htmlnode import ParentNode
from markdown_to_html import markdown_to_html_node

import os


def extract_title(page_html_node):
    if not isinstance(page_html_node, ParentNode):
        raise TypeError(
            f"extract_header expects PageNode, got {type(page_html_node)} instead"
        )
    if len(page_html_node.children) == 0 or page_html_node.children[0].tag != "h1":
        raise ValueError("Markdown pages must start with an H1 title!")

    return page_html_node.children[0].children[0].value


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown_file:
        with open(template_path) as template_file:
            markdown_content = markdown_file.read()
            template_content = template_file.read()
            root_html_node = markdown_to_html_node(markdown_content)
            title = extract_title(root_html_node)
            template_content = template_content.replace("{{ Title }}", title, 1)
            template_content = template_content.replace(
                "{{ Content }}", root_html_node.to_html(), 1
            )

            dest_dir = os.path.dirname(dest_path)
            os.makedirs(dest_dir, exist_ok=True)
            with open(dest_path, "w") as dest_file:
                dest_file.write(template_content)
