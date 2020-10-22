import wikitextparser

from typing import List

from .prototype import WikiTextHtml
from .render import (
    bold_and_italic,
    external_link,
    list_,
    parameter,
    parser_function,
    postprocess,
    preprocess,
    section,
    table,
    tag,
    template,
    wikilink,
)


class Page(WikiTextHtml):
    def __init__(self, page: str) -> None:
        self._page = page
        self._snippet = []  # type: List[str]

    def prepare(self, body) -> wikitextparser.WikiText:
        body = preprocess.begin(self, body)
        body = preprocess.pre_block(self, body)
        body = preprocess.hr_line(self, body)

        wtp = wikitextparser.parse(body)

        parameter.replace(self, wtp, [])
        parser_function.replace(self, wtp)
        template.replace(self, wtp)

        return wikitextparser.parse(wtp.string)

    def render(self) -> "Page":
        if not self.page_exists(self._page):
            self._html = f"<h2>Page {self._page} not found</h2>"
            return self

        body = self.page_load(self._page)
        wtp = self.prepare(body)

        tag.call_hooks(self, wtp)

        # Order is important. Lists inside tables will be rendered by the
        # tables; all other lists are rendered after that.
        table.replace(self, wtp)
        list_.replace(self, wtp)

        # We reload the parser, as we are going to iterate over templates
        # again. We can only do this once every reload.
        wtp = wikitextparser.parse(wtp.string)
        self._replace_snippets(wtp, "wikilink")

        wikilink.replace(self, wtp)

        # Reload the template; external links are, in contrast to other
        # entries, not automatically recalculated by wikitextparser.
        # See: https://github.com/5j9/wikitextparser/issues/74
        wtp = wikitextparser.parse(wtp.string)

        bold_and_italic.replace(self, wtp)
        external_link.replace(self, wtp)

        # We inject the TOC now; this requires a reload of the
        # wikitextparser.
        body = section.toc(self, wtp)
        wtp = wikitextparser.parse(body)
        self._replace_snippets(wtp, "post")

        section.replace(self, wtp)

        self._html = postprocess.replace(self, wtp.string)
        return self

    def store_snippet(self, snippet):
        self._snippet.append(snippet)
        return len(self._snippet) - 1

    @property
    def html(self):
        return self._html

    @property
    def page(self):
        return self._page

    def _replace_snippets(self, wikitext: wikitextparser.WikiText, stage: str):
        for template_ in reversed(wikitext.templates):
            if template_.arguments[0].value != stage:
                continue

            index = int(template_.arguments[1].value)
            template_.string = self._snippet[index]
            self._replace_snippets(template_, stage)
