import html
import urllib
import wikitextparser

from ...exceptions import InvalidWikiLink
from ...prototype import WikiTextHtml


def replace(instance: WikiTextHtml, wikilink: wikitextparser.WikiLink):
    url = wikilink.title.strip()
    if url:
        try:
            title = instance.clean_title(url)
        except InvalidWikiLink as e:
            # Errors always end with a dot, hence the [:-1].
            instance.add_error(f'{e.args[0][:-1]} (wikilink "{wikilink.string}").')
            return
    else:
        title = ""

    if wikilink.text is None:
        text = title
        if wikilink.fragment:
            text += f"#{wikilink.fragment}"
    else:
        text = wikilink.text.strip()

    title = html.escape(title)
    text = html.escape(text)

    if url == instance._page and not wikilink.fragment:
        wikilink.string = f'<strong class="selflink">{text}</strong>'
        return

    link_extra = ""

    if url and not instance.page_exists(url):
        instance.add_error(f'Linked page "{wikilink.title}" does not exist (wikilink "{wikilink.string}").')
        link_extra = ' class="new"'

    hash = ""
    if wikilink.fragment:
        hash = wikilink.fragment
        hash = f"#{hash}"

    url = instance.clean_url(url)

    if url:
        url = f"/{urllib.parse.quote(url)}"

    wikilink.string = f'<a href="{url}{hash}"{link_extra} title="{title}">{text}</a>'
