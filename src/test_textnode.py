import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("some node", "bold", "www.url.com")
        node2 = TextNode("some node", "bold", "www.url.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("some node", "bold", "www.url.com")
        node2 = TextNode("some other node", "italic")
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("some node", "bold")
        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("some node", "bold", "www.url.com")
        node2 = TextNode("some other node", "italic")
        self.assertEqual(repr(node), "TextNode(some node, bold, www.url.com)")
        self.assertEqual(repr(node2), "TextNode(some other node, italic, None)")


if __name__ == "__main__":
    unittest.main()
