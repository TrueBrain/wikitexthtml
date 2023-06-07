import wikitextparser

from ..prototype import WikiTextHtml


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for bold in reversed(wikitext.get_bolds(recursive=True)):
        # Replace the closing tag with a placeholder, of the exact same length
        # as the original text ('''). This makes sure the italic tags are still
        # in the same place.
        bold.string = f"<b>{bold.text.strip()}<B>"

    for italic in reversed(wikitext.get_italics(recursive=True)):
        italic.string = f"<i>{italic.text.strip()}</i>"

    # Replace the placeholders with the closing tags.
    wikitext.string = wikitext.string.replace("<B>", "</b>")
