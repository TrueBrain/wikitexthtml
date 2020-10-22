import wikitextparser

from .exceptions import (
    EvaluationError,
    ParserFunctionWrongArgumentCount,
)
from .helpers import (
    evaluate,
    get_argument,
)
from ...prototype import WikiTextHtml


def ifexpr(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) < 1:
        raise ParserFunctionWrongArgumentCount

    expr = get_argument(parser_function, 0)

    try:
        result = evaluate(expr)
    except EvaluationError as e:
        parser_function.string = f"Expression error: {e.args[0]}"
        return

    if result:
        parser_function.string = get_argument(parser_function, 1)
    else:
        parser_function.string = get_argument(parser_function, 2)
