import wikitextparser

from .parser_functions import (
    expr,
    if_,
    ifeq,
    ifexpr,
    ifexist,
    string,
    switch,
    url,
    variables,
)
from ..prototype import WikiTextHtml


PARSER_FUNCTIONS = {
    "#expr": expr.expr,
    "#if": if_.if_,
    "#ifeq": ifeq.ifeq,
    "#ifexpr": ifexpr.ifexpr,
    "#ifexist": ifexist.ifexist,
    "#switch": switch.switch,
    "basepagename": variables.variable,
    "currentyear": variables.variable,
    "fullpagename": variables.variable,
    "lc": string.lc,
    "lcfirst": string.lcfirst,
    "namespace": variables.variable,
    "pagename": variables.variable,
    "subpagename": variables.variable,
    "uc": string.uc,
    "ucfirst": string.ucfirst,
    "urlencode": url.encode,
}


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for parser_function in reversed(wikitext.parser_functions):
        name = parser_function.name.lower().strip()

        if name not in PARSER_FUNCTIONS:
            instance.add_error(f'Parser function "{parser_function.name}" does not exist.')
            continue

        PARSER_FUNCTIONS[name](instance, parser_function)
