text_type_text = "TEXT"
text_type_bold = "BOLD"
text_type_italic = "ITALIC"
text_type_code = "CODE"
text_type_link = "LINK"
text_type_image = "IMAGE"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, __value: object) -> bool:
        return (
            self.text == __value.text
            and self.text_type == __value.text_type
            and self.url == __value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
