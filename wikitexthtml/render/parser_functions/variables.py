import datetime
import html
import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from ...exceptions import InvalidWikiLink
from ...prototype import WikiTextHtml


def variable(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 0:
        raise ParserFunctionWrongArgumentCount

    name = parser_function.name.lower()
    if name == "currentyear":
        parser_function.string = str(datetime.datetime.now().year)
    elif name in ("pagename", "fullpagename", "basepagename"):
        parser_function.string = html.escape(instance.page)
    elif name == "subpagename":
        try:
            parser_function.string = html.escape(instance.clean_title(instance.page))
        except InvalidWikiLink as e:
            # Errors always end with a dot, hence the [:-1].
            instance.add_error(f'{e.args[0][:-1]} (parserfunction "{parser_function.string}").')
            parser_function.string = ""
    elif name == "namespace":
        parser_function.string = ""
