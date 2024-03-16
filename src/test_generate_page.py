import unittest

from generate_page import extract_title
from htmlnode import ParentNode, LeafNode


class TestGeneratePage(unittest.TestCase):

    valid_header_node = ParentNode("h1", [LeafNode(None, "header text")])

    def test_extract_header_raises_error_if_param_type_not_ParentNode(self):
        with self.assertRaises(TypeError):
            extract_title("foo")

    def test_extract_header_raises_error_if_page_is_empty(self):
        with self.assertRaises(ValueError):
            extract_title(create_page([]))

    def test_extract_header_raises_error_if_page_does_not_start_with_h1(self):
        page = create_page([LeafNode("p", "some text"), self.valid_header_node])
        with self.assertRaises(ValueError):
            extract_title(page)

    def test_extract_header_returns_header_text(self):
        page = create_page([self.valid_header_node, ParentNode("h1", [])])
        self.assertEqual(extract_title(page), "header text")


def create_page(children):
    return ParentNode("div", children)


if __name__ == "__main__":
    unittest.main()
