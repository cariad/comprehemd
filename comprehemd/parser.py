from logging import getLogger
from re import match
from typing import IO, Iterable, Optional, Tuple

from comprehemd.blocks import Block, CodeBlock, HeadingBlock
from comprehemd.blocks.empty import EmptyBlock
from comprehemd.code_patterns import CodePattern, get_code_pattern

CodeBlockMeta = Tuple[CodeBlock, CodePattern]
TryParseResult = Tuple[bool, Optional[Iterable[Block]]]


class MarkdownParser:
    """
    Markdown parser.
    """

    def __init__(self) -> None:
        self._code: Optional[CodeBlockMeta] = None
        self._line = ""
        self._logger = getLogger("comprehemd")

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

        if not pattern.fenced:
            block.collapse_source()

        yield block

        self._logger.debug("Yielding %s blank(s).", insert_blanks)

        for _ in range(insert_blanks):
            yield EmptyBlock()

    def close(self) -> Iterable[Block]:
        """
        Flushes any buffered work through the parser.
        """

        if self._line:
            self._logger.debug("Closing with a line in progress.")
            for block in self.feed("\n"):
                self._logger.debug("Yielding block formed by closing feed: %s", block)
                yield block

        for block in self._close_code(clean=False):
            self._logger.debug("Yielding block formed by closing code: %s", block)
            yield block

    def _try_parse_for_code(self, line: str) -> TryParseResult:
        """
        Attempts to parse `line` as an element of a code block.

        Returns:
            Flag to indicate if the line was handled and any blocks to yield.
        """

        if not self._code:
            new_pattern, lang = get_code_pattern(line)

            if not new_pattern:
                # This ain't the start of a code block.
                return False, None

            if not new_pattern.fenced and not self._prev_empty:
                # Unfenced blocks start only when the previous line is empty, so
                # let another handler take care of this line.
                return False, None

            new_block = CodeBlock(
                language=lang,
                source=line,
                text="" if new_pattern.fenced else new_pattern.clean(line),
            )

            # We've started a block!
            self._code = (new_block, new_pattern)
            return True, None

        block, pattern = self._code

        if pattern.is_end(line):
            if pattern.fenced:
                block.append_source(line)

            closed = self._close_code(clean=True)
            return pattern.fenced, closed

        else:
            # This isn't the end so just append the line.
            block.append(line, pattern.clean)
            return True, None

    def _try_parse_for_heading(self, line: str) -> TryParseResult:
        """
        Attempts to parse `line` as a heading.

        Returns:
            Flag to indicate if the line was handled and any blocks to yield.
        """

        heading_match = match(r"^(#{1,6})[\s]+(.*)$", line)
        if not heading_match:
            return False, None

        self._logger.debug("heading_match: %s", heading_match)

        block = HeadingBlock(
            level=len(heading_match.group(1)),
            text=heading_match.group(2),
            source=line,
        )

        return True, [block]

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

    def parse(self, line: str) -> Iterable[Block]:
        """
        Parses a complete line.
        """

        line = line.rstrip()

        self._logger.debug("Parsing line: %s", line.replace("\n", "\\n"))

        handled, blocks = self._try_parse_for_code(line)

        if blocks:
            for block in blocks:
                yield block

        # "_prev_empty" is only read by "_try_parse_for_code" so it's okay to
        # reset it now.
        self._prev_empty = not line

        if handled:
            return

        if not line:
            yield EmptyBlock()
            return

        handled, blocks = self._try_parse_for_heading(line)

        if blocks:
            for block in blocks:
                yield block

        if handled:
            return

        yield Block(text=line.rstrip(), source=line)

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
