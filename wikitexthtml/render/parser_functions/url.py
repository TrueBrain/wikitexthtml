import html
import urllib
import wikitextparser

from .helpers import get_argument
from ...prototype import WikiTextHtml


def encode(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 1:
        instance.add_error(
            f'Parser function "{parser_function.name}" expects 1 argument, '
            f"but {len(parser_function.arguments)} given."
        )
        return

    url = get_argument(parser_function, 0).strip()

    # All variables should already be HTML escaped, so unescape first,
    # as otherwise we are double encoding them.
    url = urllib.parse.quote(html.unescape(url))

    parser_function.string = url
