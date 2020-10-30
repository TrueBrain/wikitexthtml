import html
import wikitextparser

from ...prototype import WikiTextHtml


def replace(instance: WikiTextHtml, wikilink: wikitextparser.WikiLink):
    url = wikilink.title.strip()
    title = instance.clean_title(url)

    if wikilink.text is None:
        text = title
        if wikilink.fragment:
            text += f"#{wikilink.fragment}"
    else:
        text = wikilink.text.strip()

    if url == instance._page and not wikilink.fragment:
        wikilink.string = f'<strong class="selflink">{text}</strong>'
        return

    link_extra = ""

    if url and not instance.page_exists(url):
        instance.add_error(f"Linked page '{wikilink.title}' does not exist")
        link_extra = ' class="new"'

    hash = ""
    if wikilink.fragment:
        hash = wikilink.fragment
        hash = f"#{hash}"

    url = instance.clean_url(url)

    if url:
        url = f"/{html.escape(url)}"

    title = html.escape(title)
    wikilink.string = f'<a href="{url}{hash}"{link_extra} title="{title}">{text}</a>'
