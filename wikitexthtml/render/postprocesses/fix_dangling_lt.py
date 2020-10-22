from .helper import ChainHTMLParser


class HTMLParser(ChainHTMLParser):
    def handle_starttag(self, tag, attrs) -> None:
        lt_index = self.get_starttag_text().rfind("<")
        if lt_index != 0:
            # There is more than one < in this tag; assume that everything on
            # the left should be escaped, except for the last <. That is most
            # likely the real tag.
            self._result += self._html_escape(self.get_starttag_text()[:lt_index])
            self._result += self.get_starttag_text()[lt_index:]
        else:
            self._result += self.get_starttag_text()

    def handle_startendtag(self, tag, attrs):
        self._result += self.get_starttag_text()

    def handle_endtag(self, tag):
        self._result += self.get_endtag_text(tag)

    def handle_data(self, data):
        self._result += data
