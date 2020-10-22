from .helper import ChainHTMLParser
from ..config import INNER_NEEDS_P_ELEMENTS


class HTMLParser(ChainHTMLParser):
    def __init__(self, instance):
        super().__init__(instance)
        self._in_nonblock = 0
        self._block_needs_p = False
        self._never_add_p = False
        self._block = ""

    def _next_block(self):
        if self._block.strip():
            if self._block_needs_p and not self._never_add_p:
                self._result += f"<p>{self._block}</p>"
            else:
                self._result += self._block

        self._block_needs_p = False
        self._block = ""

    def _add_ref(self, value):
        self._block += value

    def handle_starttag(self, tag, attrs):
        if tag in INNER_NEEDS_P_ELEMENTS:
            self._next_block()
            self._result += self.get_starttag_text()
        else:
            self._in_nonblock += 1
            self._block += self.get_starttag_text()

        if tag in ("pre",):
            self._never_add_p = True

    def handle_startendtag(self, tag, attrs):
        if tag in INNER_NEEDS_P_ELEMENTS:
            self._next_block()
            self._result += self.get_starttag_text()
        else:
            self._block += self.get_starttag_text()

    def handle_endtag(self, tag):
        if tag in INNER_NEEDS_P_ELEMENTS:
            self._next_block()
            self._result += self.get_endtag_text(tag)
        else:
            self._in_nonblock -= 1
            self._block += self.get_endtag_text(tag)

        if tag in ("pre",):
            self._never_add_p = False

    def handle_data(self, data):
        blocks = data.split("\n\n")
        for i, block in enumerate(blocks):
            is_last_block = i == len(blocks) - 1

            if not is_last_block or self._in_nonblock == 0:
                if not is_last_block or block.strip():
                    self._block_needs_p = True

            self._block += block
            if not is_last_block:
                self._block += "\n\n"

            if not is_last_block:
                self._next_block()

    def handle_eof(self):
        self._next_block()
