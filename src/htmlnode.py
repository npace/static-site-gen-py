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
    
    def __eq__(self, __value: object) -> bool:
        return (self.tag == __value.tag
            and self.value == __value.value
            and self.children == __value.children
            and self.props == __value.props
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"