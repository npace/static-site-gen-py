import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_eq(self):
        node = HTMLNode(
            "<a>",
            "some link",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        node2 = HTMLNode(
            "<a>",
            "some link",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode(
            "<a>",
            "some link",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertNotEqual(
            node,
            HTMLNode(
                "<p>",
                "some link",
                None,
                {"href": "https://www.google.com", "target": "_blank"},
            ),
        )
        self.assertNotEqual(
            node,
            HTMLNode(
                "<a>",
                "some other link",
                None,
                {"href": "https://www.google.com", "target": "_blank"},
            ),
        )
        self.assertNotEqual(
            node,
            HTMLNode(
                "<a>",
                "some link",
                [HTMLNode()],
                {"href": "https://www.google.com", "target": "_blank"},
            ),
        )
        self.assertNotEqual(node, HTMLNode("<a>", "some link", None, {}))

    def test_base_to_html(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_props_to_html(self):
        node = HTMLNode(
            "<a>",
            "some link",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        node_without_props = HTMLNode()
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
        self.assertEqual(node_without_props.props_to_html(), "")

    def test_repr(self):
        empty_node = HTMLNode()
        node = HTMLNode(
            "<a>",
            "some link",
            [HTMLNode("<b>", "bold part")],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(repr(empty_node), "HTMLNode(None, None, None, None)")
        self.assertEqual(
            repr(node),
            "HTMLNode(<a>, some link, [HTMLNode(<b>, bold part, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})",
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        paragraph = LeafNode("p", "A paragraph of text.")
        link = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(paragraph.to_html(), "<p>A paragraph of text.</p>")
        self.assertEqual(
            link.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_no_tag_to_html(self):
        self.assertEqual(LeafNode(None, "some raw text").to_html(), "some raw text")

    def test_no_value_to_html(self):
        with self.assertRaisesRegex(ValueError, "Invalid HTML: no value"):
            LeafNode("p", None).to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_nested_to_html(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "span",
                    [LeafNode("b", "Bold text")],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><span><b>Bold text</b></span></div>",
        )

    def test_no_children_to_html(self):
        with self.assertRaisesRegex(ValueError, ("ParentNode must have children")):
            ParentNode("p", None).to_html()

    def test_no_tag_to_html(self):
        with self.assertRaisesRegex(ValueError, ("Invalid HTML: no tag")):
            ParentNode(None, None).to_html()


if __name__ == "__main__":
    unittest.main()
