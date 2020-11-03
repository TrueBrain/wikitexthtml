import wikitextparser

from . import (
    preprocess,
    parameter,
    parser_function,
)
from ..prototype import WikiTextHtml


def _render_template(instance: WikiTextHtml, template: wikitextparser.Template):
    name = template.name.strip()

    instance._templates.add(name)

    if not instance.template_exists(name):
        instance.add_error(f"Template '{name}' does not exist")

    body = instance.template_load(name)
    body = preprocess.begin(instance, body, is_transcluding=True)
    body = preprocess.hr_line(instance, body)

    wtp = wikitextparser.parse(body)

    parameter.replace(instance, wtp, template.arguments)
    parser_function.replace(instance, wtp)
    replace(instance, wtp)

    template.string = wtp.string


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText, parent: wikitextparser.WikiText = None):
    for template in reversed(wikitext.templates):
        # These snippets are meant to be replaced at the end, so hold off on
        # those for now.
        if template.name == "__snippet":
            continue

        # Run the templates breadth first. This means that if there is any
        # template inside an argument (of a template), it is resolved after
        # the parent.
        if template.parent("Template") != parent:
            continue

        _render_template(instance, template)
        replace(instance, template, template)
