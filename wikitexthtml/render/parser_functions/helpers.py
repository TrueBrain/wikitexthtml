import math
import wikitextparser

import ply.lex as lex
import ply.yacc as yacc

from .exceptions import EvaluationError

tokens = (
    "CONST",
    "DIVIDE",
    "FLOAT",
    "LPAREN",
    "MINUS",
    "MULTIPLY",
    "NUMBER",
    "PLUS",
    "POWER",
    "RPAREN",
    "UNARY",
    "ROUND",
    "LOGIC_AND",
    "LOGIC_OR",
    "EQUAL",
    "NOT_EQUAL",
    "LT",
    "GT",
    "LTE",
    "GTE",
    "MODULO",
)

constants = {
    "e": math.e,
    "pi": math.pi,
}
unary = {
    "abs": abs,
    "acos": math.acos,
    "asin": math.asin,
    "atan": math.atan,
    "ceil": math.ceil,
    "cos": math.cos,
    "exp": math.exp,
    "floor": math.floor,
    "ln": math.log,
    "not": lambda x: 0 if x != 0 else 1,
    "sin": math.sin,
    "tan": math.tan,
    "trunc": math.trunc,
}

t_DIVIDE = r"/"
t_LPAREN = r"\("
t_MINUS = r"-"
t_MULTIPLY = r"\*"
t_PLUS = r"\+"
t_POWER = r"\^"
t_RPAREN = r"\)"
t_EQUAL = r"="
t_NOT_EQUAL = r"!=|<>"
t_LT = r"<"
t_GT = r">"
t_LTE = r"<="
t_GTE = r">="


reserved = {
    "div": "DIVIDE",
    "mod": "MODULO",
    "round": "ROUND",
    "and": "LOGIC_AND",
    "or": "LOGIC_OR",
}
reserved.update({key: "CONST" for key in constants})
reserved.update({key: "UNARY" for key in unary})


t_ignore = " \t"


def t_ID(t):
    r"[a-zA-Z]+"
    if t.value.lower() not in reserved:
        raise EvaluationError(f"Unrecognized word: {t.value}")
    t.type = reserved[t.value.lower()]
    return t


def t_FLOAT(t):
    r"[+-]?\d*[.]\d*([Ee][+-]\d+)?|\d+[Ee][+-]?\d+"
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_error(t):
    raise EvaluationError(f"Illegal character: {t.value[0]}")


precedence = (
    ("left", "LOGIC_OR"),
    ("left", "LOGIC_AND"),
    ("left", "EQUAL", "NOT_EQUAL", "LT", "GT", "LTE", "GTE"),
    ("nonassoc", "ROUND"),
    ("left", "PLUS", "MINUS"),
    ("left", "MULTIPLY", "DIVIDE", "MODULO"),
    ("left", "POWER"),
    ("nonassoc", "UNARY"),
    ("nonassoc", "BINARY_UNARY"),
)


def p_parens(p):
    "expr : LPAREN expr RPAREN"
    p[0] = p[2]


def p_number(p):
    "expr : NUMBER"
    p[0] = p[1]


def p_float(p):
    "expr : FLOAT"
    p[0] = p[1]


def p_const(p):
    "expr : CONST"
    p[0] = p[1]


def p_unary_plus(p):
    "expr : PLUS expr %prec BINARY_UNARY"
    p[0] = p[2]


def p_unary_minus(p):
    "expr : MINUS expr %prec BINARY_UNARY"
    p[0] = -p[2]


def p_unary(p):
    "expr : UNARY expr"
    p[0] = unary[p[1]](p[2])


def p_power(p):
    "expr : expr POWER expr"
    p[0] = p[1] ** p[3]


def p_multiply(p):
    "expr : expr MULTIPLY expr"
    p[0] = p[1] * p[3]


def p_divide(p):
    "expr : expr DIVIDE expr"
    if p[3] == 0:
        raise EvaluationError("Division by zero")
    p[0] = p[1] / p[3]


def p_modulo(p):
    "expr : expr MODULO expr"
    p[0] = p[1] % p[3]


def p_plus(p):
    "expr : expr PLUS expr"
    p[0] = p[1] + p[3]


def p_minus(p):
    "expr : expr MINUS expr"
    p[0] = p[1] - p[3]


def p_round(p):
    "expr : expr ROUND expr"
    p[0] = round(p[1], int(p[3]))


def p_equal(p):
    "expr : expr EQUAL expr"
    p[0] = 1 if p[1] == p[3] else 0


def p_not_equal(p):
    "expr : expr NOT_EQUAL expr"
    p[0] = 1 if p[1] != p[3] else 0


def p_less_than(p):
    "expr : expr LT expr"
    p[0] = 1 if p[1] < p[3] else 0


def p_greater_than(p):
    "expr : expr GT expr"
    p[0] = 1 if p[1] > p[3] else 0


def p_less_than_equal(p):
    "expr : expr LTE expr"
    p[0] = 1 if p[1] <= p[3] else 0


def p_greater_than_equal(p):
    "expr : expr GTE expr"
    p[0] = 1 if p[1] >= p[3] else 0


def p_logic_and(p):
    "expr : expr LOGIC_AND expr"
    p[0] = p[1] & p[3]


def p_logic_or(p):
    "expr : expr LOGIC_OR expr"
    p[0] = p[1] | p[3]


def p_error(p):
    raise EvaluationError("Syntax error")


lexer = lex.lex()
parser = yacc.yacc()


def get_argument(parser_function: wikitextparser.ParserFunction, index: int):
    if len(parser_function.arguments) <= index:
        return ""

    value = parser_function.arguments[index].string[1:]
    # Only strip if this was not a multiline value
    if value.count("\n") <= 1:
        value = value.strip()
    return value


def evaluate(expr: str, as_str: bool = False):
    raw_result = parser.parse(expr)

    if not as_str:
        return raw_result

    # mediawiki used a 12-decimal precision; we do too. Also helps for the
    # cases the result is something like 14.000000000000002. By making it
    # 12 decimals it is more likely for that to become 14.
    result = str(round(raw_result, 12))

    # If the float is an integer, return as an integer
    if result.endswith(".0"):
        return str(int(raw_result))

    return result
