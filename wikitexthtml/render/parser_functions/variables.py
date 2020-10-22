import datetime
import wikitextparser

from .exceptions import ParserFunctionWrongArgumentCount
from ...prototype import WikiTextHtml


def variable(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) != 0:
        raise ParserFunctionWrongArgumentCount

    name = parser_function.name.lower()
    if name == "currentyear":
        parser_function.string = str(datetime.datetime.now().year)
    elif name in ("pagename", "fullpagename", "basepagename"):
        parser_function.string = instance.page
    elif name == "subpagename":
        parser_function.string = instance.clean_title(instance.page)
    elif name == "namespace":
        parser_function.string = ""
