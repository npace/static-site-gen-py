import unittest
from markdown_to_html import block_to_html_node, markdown_to_html_node
from markdown_block_parser import (
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


class TestBlockToHTML(unittest.TestCase):
    def assertBlockToHtml(self, block_text, block_type, expected_html):
        self.assertEqual(
            block_to_html_node(block_text, block_type).to_html(),
            expected_html,
        )

    def test_paragraph(self):
        self.assertBlockToHtml(
            "just a paragraph", block_type_paragraph, "<p>just a paragraph</p>"
        )

    def test_paragraph_multiline(self):
        self.assertBlockToHtml(
            "line1\nline2", block_type_paragraph, "<p>line1\nline2</p>"
        )

    def test_paragraph_with_inline_styles(self):
        self.assertBlockToHtml(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
            block_type_paragraph,
            "<p>This is <b>text</b> with an <i>italic</i> word and a <code>code block</code> and an "
            + '<img src="https://i.imgur.com/zjjcJKZ.png" alt="image"></img> and a <a href="https://boot.dev">link</a></p>',
        )

    def test_headings(self):
        self.assertBlockToHtml(
            "# heading 1", block_type_heading_1, "<h1>heading 1</h1>"
        )
        self.assertBlockToHtml(
            "## heading 2", block_type_heading_2, "<h2>heading 2</h2>"
        )
        self.assertBlockToHtml(
            "### heading 3", block_type_heading_3, "<h3>heading 3</h3>"
        )
        self.assertBlockToHtml(
            "#### heading 4", block_type_heading_4, "<h4>heading 4</h4>"
        )
        self.assertBlockToHtml(
            "##### heading 5", block_type_heading_5, "<h5>heading 5</h5>"
        )
        self.assertBlockToHtml(
            "###### heading 6", block_type_heading_6, "<h6>heading 6</h6>"
        )

    def test_quote(self):
        self.assertBlockToHtml(
            ">some quote\n>of two lines",
            block_type_quote,
            "<blockquote><p>some quote\nof two lines</p></blockquote>",
        )

    def test_quote_with_leading_space(self):
        self.assertBlockToHtml(
            "> some quote\n> of two lines",
            block_type_quote,
            "<blockquote><p>some quote\nof two lines</p></blockquote>",
        )

    def test_unordered_list(self):
        self.assertBlockToHtml(
            "- list\n* of\n- items",
            block_type_unordered_list,
            "<ul><li>list</li><li>of</li><li>items</li></ul>",
        )

    def test_unordered_list_with_inline_styles(self):
        self.assertBlockToHtml(
            "- **list**\n* *of*\n- `items`\n- [link](https://www.example.com)\n- ![image](https://example.com/image.jpg)",
            block_type_unordered_list,
            "<ul><li><b>list</b></li><li><i>of</i></li><li><code>items</code></li>"
            + '<li><a href="https://www.example.com">link</a></li><li><img src="https://example.com/image.jpg" alt="image"></img></li></ul>',
        )

    def test_ordered_list(self):
        self.assertBlockToHtml(
            "1. list\n2. of\n3. items",
            block_type_ordered_list,
            "<ol><li>list</li><li>of</li><li>items</li></ol>",
        )

    def test_ordered_list_with_inline_styles(self):
        self.assertBlockToHtml(
            "1. **list**\n2. *of*\n3. `items`\n4. [link](https://www.example.com)\n5. ![image](https://example.com/image.jpg)",
            block_type_ordered_list,
            "<ol><li><b>list</b></li><li><i>of</i></li><li><code>items</code></li>"
            + '<li><a href="https://www.example.com">link</a></li><li><img src="https://example.com/image.jpg" alt="image"></img></li></ol>',
        )

    def test_code(self):
        self.assertBlockToHtml(
            "```print('hello world!')```",
            block_type_code,
            "<pre><code>print('hello world!')</code></pre>",
        )

    def test_code_with_newlines(self):
        self.assertBlockToHtml(
            "```\nprint('hello')\nprint('world!')\n```",
            block_type_code,
            "<pre><code>print('hello')\nprint('world!')\n</code></pre>",
        )


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html(self):
        markdown = """
# heading 1

## heading 2

### heading 3

#### heading 4

##### heading 5

###### heading 6

regular paragraph
of two lines

- unordered
* list

1. ordered
2. list

> quote of
> two lines

```
for i in range(1,7):
    print(f'"heading {i}"')
```
"""
        expected_html = """<div><h1>heading 1</h1><h2>heading 2</h2><h3>heading 3</h3><h4>heading 4</h4><h5>heading 5</h5><h6>heading 6</h6><p>regular paragraph
of two lines</p><ul><li>unordered</li><li>list</li></ul><ol><li>ordered</li><li>list</li></ol><blockquote><p>quote of
two lines</p></blockquote><pre><code>for i in range(1,7):
    print(f'"heading {i}"')
</code></pre></div>"""
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            expected_html,
        )


if __name__ == "__main__":
    unittest.main()
