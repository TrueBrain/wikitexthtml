import wikitextparser

from .wikilinks import (
    internal,
    file,
)
from ..prototype import WikiTextHtml

WIKILINK_NAMESPACES = {
    "file": file.replace,
    "media": file.replace,
}


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for wikilink in reversed(wikitext.wikilinks):
        title = wikilink.title.lower()

        if "{{{" in title:
            # This means there was a parameter that could not be resolved;
            # this makes it an invalid wikilink, so leave it as it is.
            pass
        else:
            # If there is a :, it means there is a namespace indicator. Check
            # if we have a handler for it.
            namespace, _, _ = title.rpartition(":")
            if namespace:
                if namespace not in WIKILINK_NAMESPACES:
                    instance.add_error(
                        f'Namespace "{namespace}" is an unknown namespace (wikilink "{wikilink.string}").'
                    )
                    continue

                if WIKILINK_NAMESPACES[namespace](instance, wikilink):
                    continue
            elif ":" in title:
                # The wikilink starts with a :; this has the same meaning as
                # no :, so strip it and the rest will do its thing correctly.
                wikilink.title = wikilink.title[1:]

            internal.replace(instance, wikilink)


def register_namespace(name, handler):
    WIKILINK_NAMESPACES[name] = handler
