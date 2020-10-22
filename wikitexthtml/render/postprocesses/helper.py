from html.parser import HTMLParser

# Ensure we don't consider <script> and <style> special;
# from our perspective, they are not.
HTMLParser.CDATA_CONTENT_ELEMENTS = ()


class ChainHTMLParser(HTMLParser):
    def __init__(self, instance) -> None:
        super().__init__(convert_charrefs=False)
        self.instance = instance
        self._result = ""
        self._has_ended = False

    def _html_escape(self, body: str) -> str:
        # Similar to html.escape(), without the & -> &amp;
        return body.replace("<", "&lt;").replace(">", "&gt;")

    def feed(self, feed: str):
        super().feed(feed)
        self.close()
        return self

    def _add_ref(self, value):
        self._result += value

    def handle_entityref(self, name):
        lineno, offset = self.getpos()

        # This is a very slow way of figuring out we have a ; behind our tag.
        # Sadly, it also seems to be the only way with the html library.
        if self.rawdata.split("\n")[lineno - 1][offset:].startswith(f"&{name};"):
            self._add_ref(f"&{name};")
        else:
            self._add_ref(f"&{name}")

    def handle_charref(self, name):
        self._add_ref(f"&#{name};")

    def handle_pi(self, data):
        self.handle_data(f"<?{data}>")

    def unknown_decl(self, data):
        raise NotImplementedError(f"Unknown data in output: {data}")

    def get_endtag_text(self, tag):
        return f"</{tag}>"

    def handle_eof(self):
        pass

    @property
    def result(self):
        if not self._has_ended:
            self._has_ended = True
            self.handle_eof()

        return self._result
