---
author: Cariad Eccleston
favicon-emoji: 🤔
title: CompreheMD
---

# 🤔 CompreheMD

**CompreheMD** is a Python package for parsing Markdown documents.

<edition value="toc" hi="2" />

## Installation

CompreheMD requires Python 3.8 or later.

Install CompreheMD via pip:

```bash
pip install comprehemd
```

## MarkdownParser class

### Parsing a stream

_The Markdown document parsed in this example is [example.md](https://cariad.github.io/comprehemd/example.md)._

To read an entire text stream, call `read()`. The method yields [blocks](#blocks-classes) until the stream ends.

```python
from comprehemd import MarkdownParser

with open("docs/example.md", "r") as fp:
    for block in MarkdownParser().read(fp):
        print(block)
```

<!--edition-exec-->

### Parsing chunks

The parser can be fed ad-hoc chunks of Markdown. The `feed()` method yields all the [blocks](#blocks-classes) that the chunk completed.

After feeding the final chunk, you must call `close()` to flush and yield any buffered blocks.

```python
from comprehemd import CodeBlock, HeadingBlock, MarkdownParser

def tease(chunk: str) -> None:
    escaped = chunk.replace("\n", "\\n")
    for block in parser.feed(chunk):
        print(f'After "{escaped}", the parser yielded:')
        print(block)
        print()
    else:
        print(f'After "{escaped}", the parser did not yield.')
        print()


parser = MarkdownParser()

tease("# Feeding exam")
tease("ple\n\nThis de")
tease("monstrates chu")
tease("nked feeding.")

for block in parser.close():
    print("After closing, the parser yielded:")
    print(block)
    print()

```

<!--edition-exec-->

## Blocks classes

### Block

The `Block` class is the base of all blocks.

- `source` returns the original Markdown source for the block.
- `text` returns the meaningful text representation of the block.

### CodeBlock

The `CodeBlock` class represents a code block.

- `language` returns the language hint if one was specified.
- The block can be rendered back to Markdown by calling `render()`.

### EmptyBlock

`EmptyBlock` represents an empty line.

### HeadingBlock

The `HeadingBlock` class represents a heading.

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

- Epic ❤️ to John Gruber for developing [the original Markdown specification](https://daringfireball.net/projects/markdown/).
- This documentation was pressed by [Edition](https://github.com/cariad/edition).
