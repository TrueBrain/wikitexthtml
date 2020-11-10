import wikitextparser

from . import (
    preprocess,
    parameter,
    parser_function,
)
from ..exceptions import InvalidTemplate
from ..prototype import WikiTextHtml


def _render_template(instance: WikiTextHtml, template: wikitextparser.Template):
    name = template.name.strip()

    try:
        if not instance.template_exists(name):
            instance.add_error(f'Template "{name}" does not exist.')
    except InvalidTemplate as e:
        # Errors always end with a dot, hence the [:-1].
        instance.add_error(f'{e.args[0][:-1]} (template "{{{{{name}}}}}").')
        return

    instance._templates.add(name)
    if instance._template_path.count(name) >= 10:
        instance.add_error(
            f'Template "{name}" was transcluded itself more than ten times (recursion depth limit reached).'
        )
        return
    instance._template_path.append(name)

    body = instance.template_load(name)
    body = preprocess.begin(instance, body, is_transcluding=True)
    body = preprocess.hr_line(instance, body)

    wtp = wikitextparser.parse(body)

    parameter.replace(instance, wtp, template.arguments)
    parser_function.replace(instance, wtp)
    replace(instance, wtp)

    template.string = wtp.string

    instance._template_path.remove(name)


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
