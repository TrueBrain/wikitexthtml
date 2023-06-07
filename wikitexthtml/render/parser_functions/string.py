import wikitextparser

from .helpers import get_argument
from ...prototype import WikiTextHtml


def lc(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 1:
        instance.add_error(
            f'Parser function "{parser_function.name}" expects 1 argument, '
            f"but {len(parser_function.arguments)} given."
        )
        return

    value = get_argument(parser_function, 0).lower()
    parser_function.string = value


def uc(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 1:
        instance.add_error(
            f'Parser function "{parser_function.name}" expects 1 argument, '
            f"but {len(parser_function.arguments)} given."
        )
        return

    value = get_argument(parser_function, 0).upper()
    parser_function.string = value


def lcfirst(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 1:
        instance.add_error(
            f'Parser function "{parser_function.name}" expects 1 argument, '
            f"but {len(parser_function.arguments)} given."
        )
        return

    value = get_argument(parser_function, 0)
    parser_function.string = value[0].lower() + value[1:]


def ucfirst(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 1:
        instance.add_error(
            f'Parser function "{parser_function.name}" expects 1 argument, '
            f"but {len(parser_function.arguments)} given."
        )
        return

    value = get_argument(parser_function, 0)
    parser_function.string = value[0].upper() + value[1:]
