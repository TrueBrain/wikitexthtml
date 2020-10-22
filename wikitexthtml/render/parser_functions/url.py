import urllib
import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from .helpers import get_argument
from ...prototype import WikiTextHtml


def localurl(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) not in (1, 2):
        raise ParserFunctionWrongArgumentCount

    local_page = get_argument(parser_function, 0).strip()
    query_string = get_argument(parser_function, 1).strip()

    if query_string:
        query_string = f"?{query_string}"

    local_page = urllib.parse.quote(local_page)

    parser_function.string = f"/{local_page}{query_string}"
