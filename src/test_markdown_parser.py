import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_image,
    text_type_link,
)
from markdown_parser import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitBase(unittest.TestCase):
    def assert_split_result(self, actual, expected):
        self.assertEqual(
            actual, expected, f"\nExpected:\n{expected}\nbut got:\n{actual}"
        )


class TestSplitDelimiter(TestSplitBase):
    def test_raise_error_if_tag_not_closed(self):
        node = TextNode("Text with *open tag", text_type_text)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(
            cm.exception.args[0], "Invalid markdown, needs matching * ITALIC delimiters"
        )

    def test_split_text_just_adds_non_TextNode_objects(self):
        not_node = "foo"
        self.assert_split_result(
            split_nodes_delimiter([not_node], None, None),
            [not_node],
        )

    def test_split_one_inline_node(self):
        node = TextNode("Text with `inline code` in the middle", text_type_text)
        self.assert_split_result(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("Text with ", text_type_text),
                TextNode("inline code", text_type_code),
                TextNode(" in the middle", text_type_text),
            ],
        )

    def test_split_two_inline_nodes(self):
        node = TextNode("Text with *two* italic *nodes*", text_type_text)
        self.assert_split_result(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Text with ", text_type_text),
                TextNode("two", text_type_italic),
                TextNode(" italic ", text_type_text),
                TextNode("nodes", text_type_italic),
            ],
        )

    def test_split_leading_node(self):
        node = TextNode("*Italic* text at the start", text_type_text)
        self.assert_split_result(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Italic", text_type_italic),
                TextNode(" text at the start", text_type_text),
            ],
        )

    def test_split_trailing_node(self):
        node = TextNode("Text at the end is *italic*", text_type_text)
        self.assert_split_result(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Text at the end is ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
        )

    def test_split_multi_symbol_delimiter(self):
        node = TextNode("Text has **bold** part", text_type_text)
        self.assert_split_result(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("Text has ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" part", text_type_text),
            ],
        )

    def test_handles_multiple_input_nodes(self):
        nodes = [
            TextNode("Text has *italic* part", text_type_text),
            TextNode("Text *with* two *italic* parts", text_type_text),
        ]
        self.assert_split_result(
            split_nodes_delimiter(nodes, "*", text_type_italic),
            [
                TextNode("Text has ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" part", text_type_text),
                TextNode("Text ", text_type_text),
                TextNode("with", text_type_italic),
                TextNode(" two ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" parts", text_type_text),
            ],
        )


class TestSplitImage(TestSplitBase):
    def test_split_image_just_adds_non_TextNode_objects(self):
        not_node = "foo"
        self.assert_split_result(
            split_nodes_image([not_node]),
            [not_node],
        )

    def test_split_image_just_adds_TextNode_without_image(self):
        node = TextNode("some text without an image", text_type_text)
        self.assert_split_result(split_nodes_image([node]), [node])

    def test_split_image_preserves_trailing_link(self):
        node = TextNode(
            "![Leading image](https://www.image.com/example.jpg) and a [trailing link](https://www.example.com)",
            text_type_text,
        )
        self.assert_split_result(
            split_nodes_image([node]),
            [
                TextNode(
                    "Leading image",
                    text_type_image,
                    "https://www.image.com/example.jpg",
                ),
                TextNode(
                    " and a [trailing link](https://www.example.com)", text_type_text
                ),
            ],
        )

    def test_split_image_preserves_leading_link(self):
        node = TextNode(
            "[Leading link](https://www.example.com) and a ![trailing image](https://www.image.com/example.jpg)",
            text_type_text,
        )
        self.assert_split_result(
            split_nodes_image([node]),
            [
                TextNode(
                    "[Leading link](https://www.example.com) and a ", text_type_text
                ),
                TextNode(
                    "trailing image",
                    text_type_image,
                    "https://www.image.com/example.jpg",
                ),
            ],
        )

    def test_splits_image_with_text(self):
        node = TextNode(
            "![Leading image](https://www.image.com/example.jpg) with an inline ![image](https://i.imgur.com/zjjcJKZ.png) and a ![trailing image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        self.assert_split_result(
            split_nodes_image([node]),
            [
                TextNode(
                    "Leading image",
                    text_type_image,
                    "https://www.image.com/example.jpg",
                ),
                TextNode(" with an inline ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode(
                    "trailing image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )


class TestSplitLink(TestSplitBase):
    def test_split_link_just_adds_non_TextNode_objects(self):
        not_node = "foo"
        self.assert_split_result(
            split_nodes_link([not_node]),
            [not_node],
        )

    def test_split_link_just_adds_TextNode_without_link(self):
        node = TextNode("some text without a link", text_type_text)
        self.assert_split_result(split_nodes_link([node]), [node])

    def test_split_link_preserves_trailing_image(self):
        node = TextNode(
            "[Leading link](https://www.example.com) and a ![trailing image](https://www.example.com/image.jpg)",
            text_type_text,
        )
        self.assert_split_result(
            split_nodes_link([node]),
            [
                TextNode("Leading link", text_type_link, "https://www.example.com"),
                TextNode(
                    " and a ![trailing image](https://www.example.com/image.jpg)",
                    text_type_text,
                ),
            ],
        )

    def test_split_link_preserves_leading_image(self):
        node = TextNode(
            "![Leading image](https://www.example.com/image.jpg) and a [trailing link](https://www.example.com)",
            text_type_text,
        )
        self.assert_split_result(
            split_nodes_link([node]),
            [
                TextNode(
                    "![Leading image](https://www.example.com/image.jpg) and a ",
                    text_type_text,
                ),
                TextNode(
                    "trailing link",
                    text_type_link,
                    "https://www.example.com",
                ),
            ],
        )

    def test_splits_link_with_text(self):
        node = TextNode(
            "[Leading link](https://www.link.com/) with an inline [link](https://another.link.com) and a [trailing link](https://link.com/trailing)",
            text_type_text,
        )
        self.assert_split_result(
            split_nodes_link([node]),
            [
                TextNode(
                    "Leading link",
                    text_type_link,
                    "https://www.link.com/",
                ),
                TextNode(" with an inline ", text_type_text),
                TextNode("link", text_type_link, "https://another.link.com"),
                TextNode(" and a ", text_type_text),
                TextNode("trailing link", text_type_link, "https://link.com/trailing"),
            ],
        )


class TestTextToTextNodes(TestSplitBase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assert_split_result(
            text_to_textnodes(text),
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
        )


class TestExtractImages(unittest.TestCase):
    def test_extract_no_images(self):
        self.assertEqual(extract_markdown_images("text without images"), [])

    def test_extract_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://www.image.com/foo.jpg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://www.image.com/foo.jpg"),
            ],
        )


class TestExtractLinks(unittest.TestCase):
    def test_extract_no_links(self):
        self.assertEqual(extract_markdown_links("text without links"), [])

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
