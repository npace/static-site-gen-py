import unittest
import textwrap

from markdown_block_parser import (
    text_to_blocks,
    block_to_block_type,
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
)


class TestTextToBlocks(unittest.TestCase):
    def test_empty_string_to_empty_blocks(self):
        self.assertEqual(text_to_blocks(""), [])

    def test_single_block(self):
        self.assertEqual(text_to_blocks("some text"), ["some text"])

    def test_excessive_blank_lines_ignored(self):
        self.assertEqual(
            text_to_blocks("\n\nparagraph 1\n\n\n\n\nparagraph 2\n\n"),
            ["paragraph 1", "paragraph 2"],
        )

    def test_multiple_block(self):
        text = textwrap.dedent(
            """
            This is a **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items
            """
        )
        self.assertEqual(
            text_to_blocks(text),
            [
                "This is a **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\n"
                + "This is the same paragraph on a new line",
                "* This is a list\n" + "* with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("regular text"), block_type_paragraph)

    def test_heading_1(self):
        self.assertEqual(block_to_block_type("# heading"), block_type_heading_1)

    def test_heading_2(self):
        self.assertEqual(block_to_block_type("## heading"), block_type_heading_2)

    def test_heading_3(self):
        self.assertEqual(block_to_block_type("### heading"), block_type_heading_3)

    def test_heading_4(self):
        self.assertEqual(block_to_block_type("#### heading"), block_type_heading_4)

    def test_heading_5(self):
        self.assertEqual(block_to_block_type("##### heading"), block_type_heading_5)

    def test_heading_6(self):
        self.assertEqual(block_to_block_type("###### heading"), block_type_heading_6)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), block_type_code)
        self.assertEqual(block_to_block_type("```code```"), block_type_code)
        self.assertEqual(block_to_block_type("```code`````"), block_type_code)
        self.assertEqual(block_to_block_type("`````code```"), block_type_code)
        self.assertEqual(block_to_block_type("`````code`````"), block_type_code)

    def test_not_code(self):
        self.assertEqual(block_to_block_type("```code"), block_type_paragraph)
        self.assertEqual(block_to_block_type("code```"), block_type_paragraph)
        self.assertEqual(block_to_block_type("``code``"), block_type_paragraph)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* foo\n- bar"), block_type_unordered_list)

    def test_unordered_list_with_leading_whitespace(self):
        self.assertEqual(
            block_to_block_type("  * foo\n - bar"), block_type_unordered_list
        )

    def test_not_unordered_list(self):
        self.assertEqual(block_to_block_type("* foo\nbar"), block_type_paragraph)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. foo\n2. bar"), block_type_ordered_list)

    def test_ordered_list_with_leading_whitespace(self):
        self.assertEqual(
            block_to_block_type("  1. foo\n 2. bar"), block_type_ordered_list
        )

    def test_not_ordered_list(self):
        self.assertEqual(block_to_block_type("1. foo\nbar"), block_type_paragraph)

    def test_incorrect_ordered_list(self):
        self.assertEqual(block_to_block_type("2. foo\n1. bar"), block_type_paragraph)
        self.assertEqual(block_to_block_type("1. foo\n3. bar"), block_type_paragraph)
        self.assertEqual(block_to_block_type("2. foo\n3. bar"), block_type_paragraph)

    def test_quote(self):
        self.assertEqual(block_to_block_type(">foo\n>bar"), block_type_quote)

    def test_not_quote(self):
        self.assertEqual(block_to_block_type(">foo\nbar"), block_type_paragraph)
        self.assertEqual(block_to_block_type("foo\n>bar"), block_type_paragraph)


if __name__ == "__main__":
    unittest.main()
