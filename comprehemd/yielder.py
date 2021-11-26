from logging import getLogger
from re import match
from typing import IO, Iterable, Optional, Tuple

from comprehemd.blocks import Block, CodeBlock, HeadingBlock
from comprehemd.blocks.empty import EmptyBlock
from comprehemd.code_patterns import CodePattern, get_code_pattern
from comprehemd.outline import Outline

CodeBlockMeta = Tuple[CodeBlock, CodePattern]


class YieldingMarkdownParser:
    """
    Markdown parser.

    Arguments:
        outline: Generate an outline.
    """

    def __init__(self, outline: bool = False) -> None:
        self._code: Optional[CodeBlockMeta] = None
        self._line = ""
        self._logger = getLogger("comprehemd")
        self._outline = Outline() if outline else None

        # We claim that the previous-to-starting line was empty because it's
        # okay for a code block to start on the first line of a document:
        self._prev_empty = True

    def _close_code(self, clean: bool) -> Iterable[Block]:
        if not self._code:
            self._logger.debug("No code block to close.")
            return None

        block, pattern = self._code
        self._code = None

        if not clean and pattern.fenced:
            self._logger.debug("This is a dirty close of a fenced block: %s", block)
            for line in block.source.split("\n"):
                yield Block(line)
            self._code = None
            return

        if clean:
            self._logger.debug("This is a clean code block close.")
        else:
            self._logger.debug("This is a dirty code block close.")

        insert_blanks = (
            block.trailing_new_lines
            if not pattern.fenced and block.text.endswith("\n")
            else 0
        )

        block.collapse_text()

        yield block

        self._logger.debug("Yielding %s blank(s).", insert_blanks)

        for _ in range(insert_blanks):
            yield Block("")

    def _feed_handle_code_start(self, line: str) -> bool:
        pattern, lang = get_code_pattern(line)
        if not pattern:
            return False

        block = CodeBlock(
            language=lang,
            source=line if pattern.fenced else "",
            text="",
        )

        self._code = (block, pattern)

        if not pattern.fenced:
            self._code[0].append(line, self._code[1].clean)

        return True

    def close(self) -> Iterable[Block]:
        """
        Flushes any buffered work through the parser.
        """

        if self._line:
            self._logger.debug("Closing with a line in progress.")
            for block in self.feed("\n"):
                self._logger.debug("Yielding block formed by closing feed: %s", block)
                yield block

        if not self._code:
            return

        self._logger.debug("Closing with a code block in progress: %s", self._code)

        for block in self._close_code(clean=False):
            self._logger.debug("Yielding block formed by closing code: %s", block)
            yield block

    def parse(self, line: str) -> Iterable[Block]:
        """
        Parses a complete line.
        """

        line = line.rstrip()

        self._logger.debug("Parsing line: %s", line.replace("\n", "\\n"))

        if self._code:
            if self._code[1].is_end(line):
                fenced = self._code[1].fenced
                if fenced:
                    self._code[0].append_source(line)

                closed = self._close_code(clean=True)

                if closed:
                    for block in closed:
                        yield block

                if fenced:
                    # The line we just read is a fence and should not be parsed
                    # any further.
                    return
            else:
                # This isn't the end, so append the line:
                self._code[0].append(line, self._code[1].clean)
                return

        elif self._prev_empty:
            # We'll consider this line a new code block only if the previous
            # line was empty.
            if self._feed_handle_code_start(line):
                return

        self._prev_empty = line == "\n"

        if line == "":
            yield EmptyBlock()
            return

        heading_match = match(r"^(#{1,6})[\s]+(.*)$", line)
        if heading_match:
            self._logger.debug("heading_match: %s", heading_match)
            heading = HeadingBlock(
                level=len(heading_match.group(1)),
                text=heading_match.group(2),
                source=line,
            )
            yield heading
            return

        yield Block(text=line.rstrip(), source=line)

    def feed(self, chunk: str) -> Iterable[Block]:
        """
        Reads a chunk of a Markdown document. The chunk can be as large or small
        as required.

        Arguments:
            chunk: Next chunk of Markdown to parse.
        """

        self._logger.debug("feed: %s", chunk.replace("\n", "<\\n>"))

        wip = self._line + chunk
        lines = wip.split("\n")

        if chunk.endswith("\n"):
            # There won't be any work left over:
            self._line = ""
        else:
            # The chunk ends with an incomplete line.
            # Save that final line for later.
            self._line = lines[-1]

        # If the chunk end with \n then the final line will be empty because we
        # haven't started it yet. If the chunk does not end with \n then the
        # final line is incomplete. Either way, we want to skip the final line.
        del lines[-1]

        for line in lines:
            for block in self.parse(line):
                yield block

    def read(self, reader: IO[str]) -> Iterable[Block]:
        """
        Feeds the entire content of a text stream.

        Arguments:
            reader: Reader.
        """

        while True:
            if chunk := reader.read(1024):
                self._logger.debug("read(): Feeding chunk...")
                for block in self.feed(chunk):
                    yield block
            else:
                break

        for block in self.close():
            self._logger.debug("Yielding closing block: %s", block)
            yield block
        else:
            self._logger.debug("Close yielded no blocks.")
