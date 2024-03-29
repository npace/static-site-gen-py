from textnode import (
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        items = list(self.props.items())
        items_html = list(map(lambda item: f' {item[0]}="{item[1]}"', items))
        return "".join(items_html)

    def open_tag_to_html(self):
        return f"<{self.tag}{self.props_to_html()}>"

    def close_tag_to_html(self):
        return f"</{self.tag}>"

    def __eq__(self, __value: object) -> bool:
        return (
            self.tag == __value.tag
            and self.value == __value.value
            and self.children == __value.children
            and self.props == __value.props
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError("Invalid HTML: no value")
        html = ""
        has_tag = self.tag != None and len(self.tag) > 0
        if has_tag:
            html += self.open_tag_to_html()
        if self.value:
            html += self.value
        if has_tag:
            html += self.close_tag_to_html()
        return html

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid HTML: no tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        children_html = list(map(lambda child: child.to_html(), self.children))
        return (
            self.open_tag_to_html() + "".join(children_html) + self.close_tag_to_html()
        )

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == text_type_code:
        # leading newline renders in html <pre><code> block so it should be removed
        stripped_text = text_node.text.lstrip("\n")
        return LeafNode("code", stripped_text)
    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text node type: {text_node.text_type}")
