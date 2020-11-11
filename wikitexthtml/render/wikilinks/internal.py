import html
import urllib
import wikitextparser

from ...exceptions import InvalidWikiLink
from ...prototype import WikiTextHtml


def replace(instance: WikiTextHtml, wikilink: wikitextparser.WikiLink):
    url = wikilink.title.strip()

    text = ""
    # Always run clean_title() on the URL, as it detects URLs that are invalid
    # because of invalid namespaces, etc.
    if url:
        try:
            text = instance.clean_title(url)
        except InvalidWikiLink as e:
            # Errors always end with a dot, hence the [:-1].
            instance.add_error(f'{e.args[0][:-1]} (wikilink "{wikilink.string}").')
            return

    if wikilink.text:
        text = wikilink.text.strip()
    elif wikilink.fragment:
        text += f"#{wikilink.fragment}"

    title = html.escape(wikilink.target)
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
