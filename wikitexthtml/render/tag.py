import wikitextparser

from .tags import gallery
from ..prototype import WikiTextHtml


TAG_HOOKS = {
    "gallery": gallery.hook,
}


def call_hooks(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for tagname, func in TAG_HOOKS.items():
        for tag in reversed(wikitext.get_tags(tagname)):
            content = func(instance, tag)

            index = instance.store_snippet(content)
            tag.string = "{{" + f"__snippet|post|{index}|{tagname}" + "}}"
