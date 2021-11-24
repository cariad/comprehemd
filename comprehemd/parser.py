from logging import getLogger
from re import match
from typing import IO, Optional, Tuple

from comprehemd.blocks import Block, CodeBlock, HeadingBlock
from comprehemd.code_patterns import CodePattern, get_code_pattern
from comprehemd.outline import Outline


class MarkdownParser:
    """
    Markdown parser.

    Arguments:
        outline: Generate an outline.
    """

    def __init__(self, outline: bool = False) -> None:
        self._code_block: Optional[Tuple[CodeBlock, CodePattern]] = None
        self._line_in_progress = ""
        self._logger = getLogger("comprehemd")
        self._outline = Outline() if outline else None

        # We claim that the previous-to-starting line was empty because it's
        # okay for a code block to start on the first line of a document:
        self._prev_empty = True

    def _append_code_line(self, line: str) -> None:
        if not self._code_block:
            raise Exception("no code block to append to")
        self._logger.debug("Appending code line: %s", line)
        self._code_block[0].append_text(self._code_block[1].clean(line))
        self._code_block[0].append_source(line)

    def _close_code_block(self) -> Tuple[CodeBlock, CodePattern]:
        """
        Returns the block that was just closed.
        """

        self._logger.debug("Closing code block")

        if not self._code_block:
            raise Exception("no code block to close")

        insert_blanks = (
            self._code_block[0].trailing_empty_lines
            if not self._code_block[1].is_fenced
            and self._code_block[0].text.endswith("\n")
            else 0
        )

        self._code_block[0].collapse_text()

        if self._code_block[1].collapse:
            self._code_block[0].collapse_source()

        self._handle_code_block(self._code_block[0])

        for _ in range(insert_blanks):
            self._logger.debug("Inserting an empty block")
            self._handle_block(Block(text="", source="\n"))

        block = self._code_block
        self._code_block = None
        return block

    def _feed_handle_code_start(self, line: str) -> bool:
        pattern, lang = get_code_pattern(line)
        if not pattern:
            return False

        block = CodeBlock(
            language=lang,
            source=line if pattern.is_fenced else "",
            text="",
        )

        self._code_block = (block, pattern)

        if not pattern.is_fenced:
            self._append_code_line(line)

        return True

    def _handle_block(self, block: Block) -> None:
        self._logger.debug("block: %s", block)
        self.handle_block(block)

    def _handle_code_block(self, block: CodeBlock) -> None:
        self._logger.debug("code: %s", block)
        self.handle_code_block(block)
        self._handle_block(block)

    def _handle_heading(self, block: HeadingBlock) -> None:
        self._logger.debug("heading: %s", block)
        if self._outline:
            self._outline.add(block)
        self.handle_heading(block)
        self._handle_block(block)

    def close(self) -> None:
        """
        Flushes any buffered work through the parser.
        """

        if self._line_in_progress:
            self.feed("\n")

        if self._code_block and not self._code_block[1].is_fenced:
            self._logger.debug("Closing code block because the parser is closing")
            self._close_code_block()

    def feed(self, chunk: str) -> None:
        """
        Reads a chunk of a Markdown document. The chunk can be as large or small
        as required.

        Arguments:
            chunk: Next chunk of Markdown to parse.
        """

        self._logger.debug("feed: %s", chunk.replace("\n", "<\\n>"))

        wip = self._line_in_progress + chunk
        lines = wip.split("\n")

        if chunk.endswith("\n"):
            # There won't be any work left over:
            self._line_in_progress = ""
        else:
            # The chunk ends with an incomplete line.
            # Save that final line for later.
            self._line_in_progress = lines[-1]

        # If the chunk end with \n then the final line will be empty because we
        # haven't started it yet. If the chunk does not end with \n then the
        # final line is incomplete. Either way, we want to skip the final line.
        del lines[-1]

        for line in lines:
            self._logger.debug("line: %s", line)
            line += "\n"

            if self._code_block:
                if self._code_block[1].is_end(line):
                    self._logger.debug(
                        'Closing code block because line "%s" indicates the end of the block'
                    )
                    if self._code_block[1].is_fenced:
                        self._code_block[0].append_source(line)

                    closed = self._close_code_block()
                    if closed[1].is_fenced:
                        # The line we just read is a fence and should not be
                        # parsed any further.
                        continue
                    # The line we just read is the start of new content and so
                    # should be parsed. Carry on down.
                else:
                    self._append_code_line(line)
                    continue

            elif self._prev_empty:
                # We'll consider this line a new code block only if the previous
                # line was empty.
                handled = self._feed_handle_code_start(line)
                if handled:
                    continue

            self._prev_empty = line == "\n"

            heading_match = match(r"^(#{1,6})[\s]+(.*)$", line)
            if heading_match:
                self._logger.debug("heading_match: %s", heading_match)
                heading = HeadingBlock(
                    level=len(heading_match.group(1)),
                    text=heading_match.group(2),
                    source=line,
                )
                self._handle_heading(heading)
                continue

            self._handle_block(Block(text=line.rstrip(), source=line))

    def handle_block(self, block: Block) -> None:
        """
        Handle a block.

        Arguments:
            block: Parsed block.
        """

    def handle_code_block(self, block: CodeBlock) -> None:
        """
        Handle a code block.

        Arguments:
            block: Parsed code block.
        """

    def handle_heading(self, block: HeadingBlock) -> None:
        """
        Handle a heading.

        Arguments:
            block: Parsed heading block.
        """

    @property
    def outline(self) -> Outline:
        if not self._outline:
            raise ValueError("MarkdownParser(outline=True) to generate the outline")
        return self._outline

    def read(self, reader: IO[str]) -> None:
        """
        Feeds the entire content of a text stream.

        Arguments:
            reader: Reader.
        """

        while True:
            if chunk := reader.read(1024):
                self.feed(chunk)
                continue
            self.close()
            return
