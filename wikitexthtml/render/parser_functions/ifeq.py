import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helpers import get_argument
from ...prototype import WikiTextHtml


def ifeq(
    instance: WikiTextHtml,
    parser_function: wikitextparser.ParserFunction,
):
    if len(parser_function.arguments) < 2:
        raise ParserFunctionWrongArgumentCount

    left = get_argument(parser_function, 0)
    right = get_argument(parser_function, 1)

    if left.strip() == right.strip():
        parser_function.string = get_argument(parser_function, 2)
    else:
        parser_function.string = get_argument(parser_function, 3)
