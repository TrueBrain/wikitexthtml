import html
import urllib
import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helpers import get_argument
from ...prototype import WikiTextHtml


def encode(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 1:
        raise ParserFunctionWrongArgumentCount

    url = get_argument(parser_function, 0).strip()

    # All variables should already be HTML escaped, so unescape first,
    # as otherwise we are double encoding them.
    url = urllib.parse.quote(html.unescape(url))

    parser_function.string = url
