import wikitextparser

from .helpers import get_argument
from ...prototype import WikiTextHtml


def ifexist(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) < 1:
        instance.add_error(
            f'Parser function "{parser_function.name}" expects at least 1 argument, '
            f"but {len(parser_function.arguments)} given."
        )
        return

    page_title = get_argument(parser_function, 0)
    page_exists = instance.page_exists(page_title)

    if page_exists:
        parser_function.string = get_argument(parser_function, 1)
    else:
        parser_function.string = get_argument(parser_function, 2)
