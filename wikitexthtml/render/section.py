import regex
import wikitextparser

from collections import defaultdict
from slugify import slugify
from typing import Dict

from ..prototype import WikiTextHtml


def _remove_known_tags(title: str) -> str:
    # Remove all known tags
    wtp = wikitextparser.parse(title)
    for tag in reversed(wtp.get_tags()):
        tag.string = tag.contents
    # wikitextparser removes all important tags except <a>, as it is not valid
    # wikitext. So we have to patch that up ourself.
    title = wtp.string.replace("</a>", "")
    title = regex.sub("<a [^>]*>", "", title)
    return title.replace("<", "&lt;").replace(">", "&gt;")


def _slugify(title: str) -> str:
    slug = title.strip()
    slug = _remove_known_tags(slug)
    return slugify(slug)


def toc(instance: WikiTextHtml, wikitext: wikitextparser.WikiText) -> str:
    body = wikitext.string

    # FORCETOC will always win over NOTOC
    if "__NOTOC__" in wikitext.string and "__FORCETOC__" not in wikitext.string:
        body = body.replace("__NOTOC__", "")
        body = body.replace("__FORCETOC__", "")
        return body

    index = body.find("__TOC__")
    if index == -1:
        # Not forced and not more than 3 sections? No ToC. See fot details:
        # https://www.mediawiki.org/wiki/Manual:Table_of_contents
        # The get_sections() always returns an additional section, which is
        # the head of the page.
        if len(wikitext.get_sections()) - 1 <= 3:
            body = body.replace("__NOTOC__", "")
            body = body.replace("__FORCETOC__", "")
            return body

        index = wikitext.get_sections()[1].span[0]

    # If there is only 1 section, there is nothing to put in a TOC.
    if len(wikitext.get_sections()) == 1:
        body = body.replace("__NOTOC__", "")
        body = body.replace("__TOC__", "")
        body = body.replace("__FORCETOC__", "")
        return body

    toc = '<table id="toc">\n'
    toc += "<tbody>\n"
    toc += "<tr><td>\n"

    toc += '<div id="toctitle">\n'
    toc += "<h2>Contents</h2>\n"
    toc += "</div>\n"

    last_level = 0
    skipped_levels = []
    toc_level = 0
    toc_number = []
    for section in wikitext.get_sections():
        if not section or not section.title:
            continue

        slug = _slugify(section.title)
        title = section.title.strip()
        title = _remove_known_tags(title)
        current_level = section.level

        if current_level > last_level:
            # Keep track how much level we went up in one time; the TOC
            # level always goes up by one.
            skipped_levels.append(current_level - last_level)

            toc_level += 1
            toc_number.append(1)

            toc += "<ul>\n"
        elif current_level < last_level:
            change = last_level - current_level

            # Check how many levels we jump back. This means you can skip
            # levels between chapters, but the TOC won't show an empty
            # chapter in between.
            level_change = 0
            while skipped_levels[-1] <= change:
                change -= skipped_levels[-1]
                skipped_levels.pop()
                level_change += 1
            skipped_levels[-1] -= change

            # For the amount of levels we changed, close the lists.
            if level_change > 0:
                for _ in range(level_change):
                    toc += "</li>\n"
                    toc += "</ul>\n"
                    toc_number.pop()
                    toc_level -= 1

            toc_number[-1] += 1
            toc += "</li>\n"
        else:
            # Level was the same, so continue to the next.
            toc_number[-1] += 1
            toc += "</li>\n"

        toc += f'<li class="toclevel-{toc_level}">\n'
        toc += f'<a href="#{slug}">\n'
        toc += f'<span class="tocnumber">{".".join([str(t) for t in toc_number])}</span>\n'
        toc += f'<span class="toctext">{title}</span>\n'
        toc += "</a>\n"

        last_level = current_level

    # Close all remaining lists.
    for _ in range(toc_level):
        toc += "</li>\n"
        toc += "</ul>\n"

    toc += "</td></tr>\n"
    toc += "</tbody>\n"
    toc += "</table>\n"

    body = body[:index] + toc + body[index:]
    body = body.replace("__TOC__", "")
    body = body.replace("__NOTOC__", "")
    body = body.replace("__FORCETOC__", "")
    return body


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    slugs = defaultdict(int)  # type: Dict[str, int]

    # Calculate how many times we see the same slug.
    # We want the sections to be numbered from top to bottom. So we have to do
    # this in a separate step, as we run the sections in reverse while
    # modifying them.
    for section in wikitext.get_sections():
        if not section or not section.title:
            continue

        slugs[_slugify(section.title)] += 1

    for section in reversed(wikitext.get_sections()):
        if not section:
            continue

        if section.title:
            slug = _slugify(section.title)
            if slugs[slug] != 1:
                slugs[slug] -= 1
                slug = f"{slug}_{slugs[slug] + 1}"

            title = section.title.strip()

            content = f"<h{section.level}>"
            content += f'<a class="anchor" id="{slug}" href="#{slug}"></a>'
            content += f'<a name="{slug}" id="{slug}"></a>'
            content += f'<span class="mw-headline" id="{slug}">{title}</span>'
            content += f"</h{section.level}>\n"
        else:
            content = ""

        section.string = content + section.contents
