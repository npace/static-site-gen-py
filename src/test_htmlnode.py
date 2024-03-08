import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_eq(self):
        node = HTMLNode("<a>", "some link", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("<a>", "some link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("<a>", "some link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, HTMLNode("<p>", "some link", None, {"href": "https://www.google.com", "target": "_blank"}))
        self.assertNotEqual(node, HTMLNode("<a>", "some other link", None, {"href": "https://www.google.com", "target": "_blank"}))
        self.assertNotEqual(node, HTMLNode("<a>", "some link", [HTMLNode()], {"href": "https://www.google.com", "target": "_blank"}))
        self.assertNotEqual(node, HTMLNode("<a>", "some link", None, {}))

    def test_base_to_html(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_props_to_html(self):
        node = HTMLNode("<a>", "some link", None, {"href": "https://www.google.com", "target": "_blank"})
        node_without_props = HTMLNode()
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node_without_props.props_to_html(), '')

    def test_repr(self):
        empty_node = HTMLNode()
        node = HTMLNode("<a>", "some link", [HTMLNode("<b>", "bold part")], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(empty_node), "HTMLNode(None, None, None, None)")
        self.assertEqual(repr(node), "HTMLNode(<a>, some link, [HTMLNode(<b>, bold part, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})")


if __name__ == "__main__":
    unittest.main()