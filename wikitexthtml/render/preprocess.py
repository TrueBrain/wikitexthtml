import regex
import wikitextparser

from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

from . import bold_and_italic
from .config import VALID_TAGS
from ..prototype import WikiTextHtml

COMMENT_PATTERN = regex.compile(r"<!--[\s\S]*?(?>-->|\Z)")
INCLUDEONLY_PATTERN = regex.compile(r"<includeonly>([\s\S]*?)(?></includeonly>|\Z)")
NOINCLUDE_PATTERN = regex.compile(r"<noinclude>([\s\S]*?)(?></noinclude>|\Z)")
NOWIKI_IN_PRE_PATTERN = regex.compile(r"<pre>\s*<nowiki>([\s\S]*?)<\/nowiki>\s*<\/pre>")
NOWIKI_PATTERN = regex.compile(r"<nowiki>([\s\S]*?)(?></nowiki>|\Z)")
ONLYINCLUDE_PATTERN = regex.compile(r"<onlyinclude>([\s\S]*?)(?></onlyinclude>|\Z)")
PRE_PATTERN = regex.compile(r"<pre>([\s\S]*?)(?></pre>|\Z)")
SYNTAXHIGHLIGHT_PATTERN = regex.compile(
    r"<syntaxhighlight( lang=\"(?P<lang>[^\"]+)\")?"
    r"(?P<line> line( start=\"(?P<lineStart>\d+)\")?)?>"
    r"(?P<code>[\s\S]*?)(</syntaxhighlight>|\Z)"
)


def _html_escape(body: str) -> str:
    # Similar to html.escape(), without the & -> &amp;
    return body.replace("<", "&lt;").replace(">", "&gt;")


def begin(instance: WikiTextHtml, body: str, is_transcluding: bool = False) -> str:
    # <onlyinclude> content is kept if we are transcluding, before any other
    # preprocessing is done (https://www.mediawiki.org/wiki/Transclusion).
    if "<onlyinclude>" in body:
        if is_transcluding:
            body = "".join([match[1] for match in ONLYINCLUDE_PATTERN.finditer(body)])
        else:
            # <onlyinclude> has no effect if not transcluding; remove the tags.
            body = ONLYINCLUDE_PATTERN.sub(r"\1", body)

    # Using a <nowiki> inside a <pre> is pointless, but in the old days
    # mediawiki did it like this, so many people still tend to do so.
    body = regex.sub(NOWIKI_IN_PRE_PATTERN, r"<pre>\1</pre>", body)

    # It is not possible to <nowiki> a <onlyinclude> tag, but you can do it
    # with any other tag.
    for match in reversed(list(NOWIKI_PATTERN.finditer(body))):
        content = match[1]
        content = _html_escape(content)

        index = instance.store_snippet(content)
        start, end = match.span()
        body = body[:start] + "{{" + f"__snippet|post|{index}|nowiki" + "}}" + body[end:]

    # Remove existing <pre> blocks and HTML escape all their content. A <pre>
    # block in wikitext acts like a <nowiki> block, but any <nowiki> inside a
    # <pre> block has its <nowiki> tags removed.
    for match in reversed(list(PRE_PATTERN.finditer(body))):
        content = match[1]
        content = _html_escape(content)

        index = instance.store_snippet(f"<pre>{content}</pre>")
        start, end = match.span()
        body = body[:start] + "{{" + f"__snippet|post|{index}|pre" + "}}" + body[end:]

    # Remove all comments from the page
    body = regex.sub(COMMENT_PATTERN, r"", body)

    # Remove / keep <noinclude> and <includeonly> depending on if we are
    # transcluding the page (https://www.mediawiki.org/wiki/Transclusion).
    if is_transcluding:
        body = NOINCLUDE_PATTERN.sub(r"", body)
        body = INCLUDEONLY_PATTERN.sub(r"\1", body)
    else:
        body = NOINCLUDE_PATTERN.sub(r"\1", body)
        body = INCLUDEONLY_PATTERN.sub(r"", body)

    return body


def hr_line(instance: WikiTextHtml, body: str) -> str:
    return regex.sub(r"\n----+\n", r"\n\n<hr />\n", body)


def highlight_syntax(instance: WikiTextHtml, body: str) -> str:
    # Use Pygments to generate highlighted code blocks.

    # The SYNTAXHIGHLIGHT_PATTERN Generates 6 groups:
    #   The first group (match[0]) is the entire match.
    #   The third group ('lang') is the language.
    #   The fourth group ('line') is a boolean to specify line numbering.
    #   The fifth group ('linestart') is the line number to start at.
    #   The sixth group ('code') is the code to highlight.

    for match in reversed(list(SYNTAXHIGHLIGHT_PATTERN.finditer(body))):
        lang = match.group("lang")
        line_boolean = True if match.group("line") else False
        line_start = int(match.group("lineStart")) if match.group("lineStart") else 1
        content = match.group("code")

        try:
            # Try to find a lexer based on the text captured by the 'lang' group.
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            # Either there was no language specified, or the language is not supported by Pygments.
            try:
                lexer = guess_lexer(content)
                if lang:
                    instance.add_error(
                        f"Syntax highlighting: unknown language '{lang}'. (Using best guess: {lexer.name})"
                    )
                else:
                    instance.add_error(f"Syntax highlighting: language not specified. (Using best guess: {lexer.name})")
            except ClassNotFound:
                lexer = None
                instance.add_error("Syntax highlighting: unable to guess language, will render without highlighting.")

        if lexer:
            content = highlight(
                content, lexer, HtmlFormatter(linenos=line_boolean, linenostart=line_start, cssclass="syntaxhighlight")
            )
        else:
            # At this point, fall back to unformatted <pre> blocks.
            content = "<pre>{}</pre>".format(_html_escape(content))

        index = instance.store_snippet(content)
        start, end = match.span()

        # Re-insert formatted block.
        body = body[:start] + "{{" + f"__snippet|post|{index}|syntaxhighlight" + "}}" + body[end:]

    return body


def replace_syntax_highlight_with_pre(instance: WikiTextHtml, body: str) -> str:
    # If we don't want to color the syntax, remove all <syntaxhighlight> tags
    # and replace them with <pre> tags.
    return SYNTAXHIGHLIGHT_PATTERN.sub(r"<pre>\g<code></pre>", body)


def pre_block(instance: WikiTextHtml, body: str) -> str:
    # Generate a shadow copy with all the wikitext stripped out. This allows
    # us to see which lines starting with a space should be embraced with a
    # <pre> block.
    shadow = wikitextparser.parse(body)
    for node in reversed(shadow.wikilinks):
        node.string = "!" * len(node.string)
    for node in reversed(shadow.parser_functions):
        node.string = "!" * len(node.string)
    for node in reversed(shadow.templates):
        node.string = "!" * len(node.string)

    # Based on the shadow, replace what should become <pre> blocks in the
    # body.
    for match in reversed(list(regex.finditer(r"^ (.*?)$", shadow.string, flags=regex.MULTILINE))):
        # Line-starters for tables shouldn't be put in a pre-block. We do not
        # filter tables out completely, as inside a row can be things we want
        # to put in a pre-block. This is not perfect, as doing something like:
        #  !! important !!
        # Will now not be put in a pre-block.
        if match[1].lstrip().startswith(("!", "|", "{|", "|}")):
            continue

        line = match[1].lower()
        # If there is any tag inside, don't put the match in a pre-block.
        for tag in VALID_TAGS:
            if tag in ("b", "i", "code"):
                continue

            if f"<{tag}>" in line or f"<{tag} " in line or f"</{tag}" in line:
                break
        else:
            start, end = match.span()
            line = body[start + 1 : end]  # Skip the whitespace

            # We change b/i back into the wikitext format.
            line = line.replace("<b>", "''").replace("</b>", "''").replace("<i>", "'''").replace("</i>", "'''")
            # And remove code-blocks (they are of little use inside a
            # pre-block).
            line = line.replace("<code>", "").replace("</code>", "")
            line = _html_escape(line)

            # Convert bold / italic back into their HTML format
            wtp = wikitextparser.parse(line)
            bold_and_italic.replace(instance, wtp)
            # In case any of the snippets got in. This happens when someone
            # for example does " <nowiki>[[Link|Tekst]]</nowiki>"
            # Observe that this is fully unneeded to do so, as anything on a
            # line starting with a space is implicit in a nowiki-block.
            instance._replace_snippets(wtp, "post")
            line = wtp.string

            body = body[:start] + f"<pre>{line}</pre>" + body[end:]

    body = body.replace("</pre>\n<pre>", "\n")
    body = regex.sub(r"<pre>[\s]*</pre>", r"", body)

    # Replace the new pre-blocks with snippets too, so they are no longer
    # processed by the rest of the pipeline.
    for match in reversed(list(PRE_PATTERN.finditer(body))):
        content = match[1]
        # TODO -- We should escape everything except "b", "i", and "code".

        index = instance.store_snippet(f"<pre>{content}</pre>")
        start, end = match.span()
        body = body[:start] + "{{" + f"__snippet|post|{index}|pre" + "}}" + body[end:]

    return body
