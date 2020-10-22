import logging
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

log = logging.getLogger(__name__)


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
    "localurl": url.localurl,
    "namespace": variables.variable,
    "pagename": variables.variable,
    "subpagename": variables.variable,
    "uc": string.uc,
    "ucfirst": string.ucfirst,
}


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for parser_function in reversed(wikitext.parser_functions):
        name = parser_function.name.lower().strip()

        if name in PARSER_FUNCTIONS:
            PARSER_FUNCTIONS[name](instance, parser_function)
        else:
            log.error(f"Unknown parser function {parser_function.name}")
