from .postprocesses import (
    add_p_blocks,
    clean_html,
    fix_dangling_lt,
)
from ..prototype import WikiTextHtml


def replace(instance: WikiTextHtml, body: str):
    body = fix_dangling_lt.HTMLParser(instance).feed(body).result
    body = clean_html.HTMLParser(instance).feed(body).result
    body = add_p_blocks.HTMLParser(instance).feed(body).result
    return body
