import wikitextparser

from .exceptions import EvaluationError
from .helpers import (
    evaluate,
    get_argument,
)
from ...prototype import WikiTextHtml


def expr(instance: WikiTextHtml, parser_function: wikitextparser.ParserFunction):
    if len(parser_function.arguments) < 1:
        instance.add_error(
            f'Parser function "{parser_function.name}" expects at least argument, '
            f"but {len(parser_function.arguments)} given."
        )
        return

    expr = get_argument(parser_function, 0)

    try:
        result = evaluate(expr, as_str=True)
    except EvaluationError as e:
        result = f"Expression error: {e.args[0]}"

    parser_function.string = result
