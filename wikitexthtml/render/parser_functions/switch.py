import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helpers import get_argument
from ...prototype import WikiTextHtml


def switch(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    branch = get_argument(parser_function, 0).strip()

    explicit_default = None
    positional_default = None
    fallthrough = False

    for argument in parser_function.arguments[1:]:
        # Fallthough cases are positional from our perspective
        if argument.positional:
            name = argument.value.strip()
        else:
            name = argument.name.strip()

        if name == "#default":
            explicit_default = argument.value
        # The last positional argument is the positional default, which is
        # used if no explicit default is set.
        if argument.positional:
            positional_default = argument.value.strip()

        # Find the fallthrough value
        if fallthrough and not argument.positional:
            value = argument.value
            break

        if name == branch:
            if argument.positional:
                fallthrough = True
            else:
                value = argument.value
                break
    else:
        if explicit_default is not None:
            value = explicit_default
        elif positional_default is not None:
            value = positional_default
        else:
            value = ""

    # Only strip if this was not a multiline value
    if value.count("\n") <= 1:
        value = value.strip()
    parser_function.string = value
