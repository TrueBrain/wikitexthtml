import logging
import wikitextparser

from .wikilinks import (
    internal,
    file,
)
from ..prototype import WikiTextHtml

log = logging.getLogger(__name__)

WIKILINK_NAMESPACES = {
    "file": file.replace,
    "media": file.replace,
}


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for wikilink in reversed(wikitext.wikilinks):
        title = wikilink.title.lower().strip()

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
                    log.error(f"Unregistered link namespace: {namespace}")
                    continue

                if WIKILINK_NAMESPACES[namespace](instance, wikilink):
                    continue

            internal.replace(instance, wikilink)


def register_namespace(name, handler):
    WIKILINK_NAMESPACES[name] = handler
