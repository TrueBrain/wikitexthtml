import wikitextparser

from ..prototype import WikiTextHtml


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for bold in reversed(wikitext.get_bolds(recursive=True)):
        bold.string = f"<b>{bold.text.strip()}</b>"

    for italic in reversed(wikitext.get_italics(recursive=True)):
        italic.string = f"<i>{italic.text.strip()}</i>"
