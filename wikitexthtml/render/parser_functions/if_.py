import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helpers import get_argument
from ...prototype import WikiTextHtml


def if_(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    condition = get_argument(parser_function, 0)

    if condition.strip():
        parser_function.string = get_argument(parser_function, 1)
    else:
        parser_function.string = get_argument(parser_function, 2)
