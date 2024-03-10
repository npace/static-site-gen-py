import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_italic,
)
from markdown_parser import split_nodes_delimiter


class TestSplitDelimiter(unittest.TestCase):
    def test_raise_error_if_tag_not_closed(self):
        node = TextNode("Text with *open tag", text_type_text)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(
            cm.exception.args[0], "Invalid markdown, needs matching * ITALIC delimiters"
        )

    def test_split_just_adds_non_TextNode_objects(self):
        not_node = "foo"
        self.__assert_split_result(
            split_nodes_delimiter([not_node], None, None),
            [not_node],
        )

    def test_split_one_inline_node(self):
        node = TextNode("Text with `inline code` in the middle", text_type_text)
        self.__assert_split_result(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("Text with ", text_type_text),
                TextNode("inline code", text_type_code),
                TextNode(" in the middle", text_type_text),
            ],
        )

    def test_split_two_inline_nodes(self):
        node = TextNode("Text with *two* italic *nodes*", text_type_text)
        self.__assert_split_result(
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
        self.__assert_split_result(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Italic", text_type_italic),
                TextNode(" text at the start", text_type_text),
            ],
        )

    def test_split_trailing_node(self):
        node = TextNode("Text at the end is *italic*", text_type_text)
        self.__assert_split_result(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Text at the end is ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
        )

    def test_split_multi_symbol_delimiter(self):
        node = TextNode("Text has **bold** part", text_type_text)
        self.__assert_split_result(
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
        self.__assert_split_result(
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

    def __assert_split_result(self, actual, expected):
        self.assertEqual(
            actual, expected, f"\nExpected:\n{expected}\nbut got:\n{actual}"
        )


if __name__ == "__main__":
    unittest.main()
