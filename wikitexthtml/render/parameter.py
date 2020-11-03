import re
import wikitextparser

from typing import List

from ..prototype import WikiTextHtml


def _lookup_nth_positional(function_arguments: List[wikitextparser.Argument], index: int):
    for function_argument in function_arguments:
        if not function_argument.positional:
            continue

        index -= 1
        if index == 0:
            return function_argument.value
    return None


def _lookup_named(function_arguments: List[wikitextparser.Argument], name):
    for function_argument in function_arguments:
        if function_argument.positional:
            continue

        if function_argument.name.strip() == name:
            return function_argument.value
    return None


def replace(
    instance: WikiTextHtml, wikitext: wikitextparser.WikiText, function_arguments: List[wikitextparser.Argument]
):
    for parameter in reversed(wikitext.parameters):
        # Check if the parameter can be found by name.
        # A position value, like {{{4}}} can also be found by name if the
        # caller used the |4=..| syntax. If this fails, we fall back to
        # search for the 4th positional argument in this example.
        value = _lookup_named(function_arguments, parameter.name)

        if value is None and parameter.name.isnumeric():
            index = int(parameter.name)
            value = _lookup_nth_positional(function_arguments, index)

        if value is None:
            if parameter.default is not None:
                value = parameter.default
            else:
                value = "{{{" + parameter.name + "}}}"

        # Only strip if this was not a multiline value
        if value.count("\n") < 2:
            value = value.strip()
        parameter.string = value

    # It is possible "[[{{{link|}}}|Text]]"" is now "[[|Text]]". This is not
    # a valid wikilink, but the | will be picked up by parser-functions. As
    # such, remove the problem by escaping it. For details, see:
    # https://github.com/5j9/wikitextparser/pull/78#issuecomment-714227623
    if "[[|" in wikitext.string:
        wikitext.string = re.sub(r"\[\[\|([^\]]*)\]\]", r"%5B%5B%7C\1%5D%5D", wikitext.string)
