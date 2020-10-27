import wikitextparser

from ..prototype import WikiTextHtml


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    # Count how many links in brackets without text we have; as we replace
    # them in reverse, we need to know the count from the start.
    bracket_count = len(
        [True for external_link in wikitext.external_links if not external_link.text and external_link.in_brackets]
    )

    for external_link in reversed(wikitext.external_links):
        url = external_link.url.strip().replace('"', "&quot;").replace("'", "&#x27;")
        extra = ""

        if external_link.text:
            text = external_link.text.strip()
        elif external_link.in_brackets:
            text = f"[{bracket_count}]"
            bracket_count -= 1
        else:
            # If the URL ends with a '.', ',' and ';', it is likely it wasn't
            # meant to be part of the URL.
            while url.endswith((".", ",", ";")):
                extra = f"{url[-1]}{extra}"
                url = url[:-1]

            # If the URL ends with a ) and there are no *, it is likely it
            # wasn't meant to be part of the URL.
            if url.endswith(")") and url.count("(") != url.count(")"):
                extra = f"{url[-1]}{extra}"
                url = url[:-1]

            text = url

        external_link.string = f'<a class="external" href="{url}" target="_new">{text}</a>{extra}'
