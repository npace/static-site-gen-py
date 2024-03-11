import unittest
import textwrap

from markdown_block_parser import (
    text_to_blocks,
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


if __name__ == "__main__":
    unittest.main()
