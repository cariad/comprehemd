---
author: Cariad Eccleston
favicon-emoji: 🤔
title: CompreheMD
---

# 🤔 CompreheMD

**CompreheMD** is a Python package for parsing Markdown documents.

The parser currently identifies:

- Headings
- Code blocks
    - Backtick and tilde fenced, with language
    - Indented

Everything else is currently recognised as plain text.

<edition value="toc" />

## Quick start

### Installation

CompreheMD requires Python 3.8 or later.

Install CompreheMD via pip:

```bash
pip install comprehemd
```

### Example

This example simply prints the parsed blocks of an [example document](https://github.com/cariad/comprehemd/blob/main/docs/example.md):

```python
from comprehemd import Block, MarkdownParser

class CustomMarkdownParser(MarkdownParser):
    def handle_block(self, block: Block) -> None:
        print(block)

with open("docs/example.md", "r") as f:
    CustomMarkdownParser().read(f)
```

<!--edition-exec-->

## Usage

### MarkdownParser

When fed chunks of Markdown, the `MarkdownParser` class calls handler functions as and when blocks are recognised.

For example, this code will print only the headings in a document:

```python
from comprehemd import HeadingBlock, MarkdownParser

class CustomMarkdownParser(MarkdownParser):
    def handle_heading(self, block: HeadingBlock) -> None:
        print(block)

with open("docs/example.md", "r") as f:
    CustomMarkdownParser().read(f)
```

<!--edition-exec-->

#### Handlers

`handle_block(block: Block)` is called for every parsed block.

`handle_code_block(block: CodeBlock)` is called for every parsed code block.

`handle_heading(block: HeadingBlock)` is called for every parsed heading block.

#### Feeding

To feed a text stream into the parser, call `read(reader: IO[str])`.

To feed in your own ad-hoc chunks, call `feed(chunk: str)`. Each chunk can be as large or small as suits. Call `close()` at the end to ensure buffered work is flushed through.

### Outline

Create the parser with `MarkdownParser(outline=True)` to generate an outline as the document is parsed.

```python
from comprehemd import MarkdownParser

parser = MarkdownParser(outline=True)

with open("docs/example.md", "r") as f:
    parser.read(f)

print(parser.outline)
```

<!--edition-exec-->

The `Outline` class exposes its items on the `root` property.

An outline can also be rendered to Markdown via the `render()` method.

### Blocks

#### Block

The `Block` class is the base of all blocks.

- `source` returns the original Markdown source for the block.
- `text` returns the meaningful text representation of the block.

#### CodeBlock

The `CodeBlock` class represents a code block.

- `language` returns the language hint if one was specified. For example, ````json` describes "json".
- The block can be rendered to Markdown with any fence type via the `render(writer: IO[str], fence: Fence)` method.

#### HeadingBlock

The `HeadingBlock` class represents a heading.

- `anchor` returns the heading's anchor.
- `level` returns the heading's level (i.e. 1 for the top-most heading, down to 6 for the lowest).

## Project

### Contributing

To contribute a bug report, enhancement or feature request, please raise an issue at [github.com/cariad/comprehemd/issues](https://github.com/cariad/comprehemd/issues).

If you want to contribute a code change, please raise an issue first so we can chat about the direction you want to take.

### Licence

CompreheMD is released at [github.com/cariad/comprehemd](https://github.com/cariad/comprehemd) under the MIT Licence.

See [LICENSE](https://github.com/cariad/comprehemd/blob/main/LICENSE) for more information.

### Author

Hello! 👋 I'm **Cariad Eccleston** and I'm a freelance DevOps and backend engineer. My contact details are available on my personal wiki at [cariad.earth](https://cariad.earth).

Please consider supporting my open source projects by [sponsoring me on GitHub](https://github.com/sponsors/cariad/).

### Acknowledgements

- This documentation was pressed by [Edition](https://github.com/cariad/edition).
