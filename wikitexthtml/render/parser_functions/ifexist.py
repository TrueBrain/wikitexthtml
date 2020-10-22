import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helpers import get_argument
from ...prototype import WikiTextHtml


def ifexist(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    page_title = get_argument(parser_function, 0)
    page_exists = instance.page_exists(page_title)

    if page_exists:
        parser_function.string = get_argument(parser_function, 1)
    else:
        parser_function.string = get_argument(parser_function, 2)
