import html
import urllib
import wikitextparser

from typing import (
    Any,
    Dict,
)

from ...exceptions import InvalidWikiLink
from ...prototype import WikiTextHtml


def replace(instance: WikiTextHtml, wikilink: wikitextparser.WikiLink):
    is_image = False
    is_media = False

    if wikilink.title.lower().startswith("file:"):
        filename = wikilink.title[5:]
        is_image = True
    elif wikilink.title.lower().startswith("media:"):
        filename = wikilink.title[6:]
        is_media = True
    else:
        raise NotImplementedError(f"Unknown wikilink file {wikilink.title}")

    url = filename.strip()

    try:
        if not instance.file_exists(url):
            instance.add_error(f'Upload "{wikilink.title}" does not exist (wikilink "{wikilink.string}").')
            file_not_found = True
        else:
            file_not_found = False
    except InvalidWikiLink as e:
        # Errors always end with a dot, hence the [:-1].
        instance.add_error(f'{e.args[0][:-1]} (wikilink "{wikilink.string}").')
        return True

    title = ""
    options = {
        "height": None,
        "horizontal": None,
        "alt": None,
        "link": instance.file_get_link(url),
        "url": url,
        "title": None,
        "vertical": "middle",
        "width": None,
    }  # type: Dict[str, Any]
    thumb = False
    magnify = False
    frameless = False
    border = False

    if wikilink.text:
        # If there is any text, they are parameters divided by |
        raw_options = wikilink.text.split("|")

        for raw_option in raw_options:
            option = raw_option.lower().strip()

            if option in ("left", "center", "right", "none"):
                # Only accept the first time a user sets the horizontal setting
                if options["horizontal"] is None:
                    options["horizontal"] = option
                else:
                    instance.add_error(
                        f'Image "{wikilink.title}" sets both "{option}" and "{options["horizontal"]}"; '
                        f'please set either one (wikilink "{wikilink.string}").'
                    )
            elif option in ("baseline", "sub", "super", "top", "text-top", "middle", "bottom", "text-bottom"):
                options["vertical"] = option
            elif option == "frameless":
                frameless = True
            elif option in ("thumb", "frame"):
                # Only accept the first time a user sets the frame
                if thumb is False:
                    thumb = True
                    if option == "thumb":
                        magnify = True
                else:
                    previous_option = "frame"
                    if magnify:
                        previous_option = "thumb"
                    instance.add_error(
                        f'Image "{wikilink.title}" sets both "{option}" as "{previous_option}"; '
                        f'please set either one (wikilink "{wikilink.string}").'
                    )
            elif option == "border":
                border = True
            elif option.endswith("px"):
                option = option[:-2]
                if "x" in option:
                    width, _, height = option.partition("x")
                    if width:
                        options["width"] = int(width)
                    options["height"] = int(height)
                else:
                    width = option
                    options["width"] = int(width)
            elif option.startswith("link="):
                options["link"] = option[5:]
                options["title"] = option[5:]

                if options["link"].startswith(":"):
                    options["link"] = options["link"][1:]

                if options["link"] and not options["link"].startswith(("http://", "https://")):
                    options["link"] = f"/{options['link']}"
            elif option.startswith("alt="):
                options["alt"] = option[4:]
            elif title == "":
                # Anything we don't understand has to be the title .. we hope
                title = raw_option.strip()
            else:
                instance.add_error(
                    f'Image "{wikilink.title}" has option "{title}" and "{option}"; '
                    f'either one of them is not a valid option (wikilink "{wikilink.string}").'
                )

                # We cannot tell which of the two was meant to the the title.
                # We pick the last option we saw as a title, and throw an
                # error to the person editing.
                title = raw_option.strip()

    extra_a = ""
    extra_img = ""

    if not title:
        if options["title"]:
            title = options["title"]
        elif not thumb:
            title = options["link"]
        else:
            title = ""

    if not frameless:
        extra_a += ' class="image"'
    if is_media:
        extra_a += ' class="internal"'

    if frameless:
        extra_a += f' title="{html.escape(title)}"'
    elif is_image and not thumb:
        extra_a += f' title="{html.escape(title)}"'
        if not options["alt"]:
            options["alt"] = title

    if options["width"]:
        extra_img += f' width="{options["width"]}"'
    if options["height"]:
        extra_img += f' height="{options["height"]}"'

    if thumb:
        extra_img += ' class="thumbimage"'
    elif border:
        extra_img += ' class="thumbborder"'

    # Thumbs are by default floating right
    if thumb and options["horizontal"] is None:
        options["horizontal"] = "right"

    if options["alt"]:
        extra_img += f' alt="{html.escape(options["alt"])}"'

    if file_not_found:
        href = urllib.parse.quote(instance.file_get_link(url))
        content = f'<a href="{href}" class="new">{wikilink.title}</a>'
    else:
        if is_image:
            if thumb:
                # TODO -- What is the default value for this?
                thumb_width = options["width"]
            else:
                thumb_width = None

            img = instance.file_get_img(url, thumb=thumb_width)
            img = urllib.parse.quote(img)
            content = f'<img src="{img}"{extra_img} />'
        else:
            content = title

        if options["link"].startswith(("http://", "https://")):
            content = f'[{options["link"]} {content}]'
        elif options["link"]:
            href = urllib.parse.quote(options["link"])
            content = f'<a href="{href}"{extra_a}>{content}</a>'
        # TODO -- If thumb, load a thumb-url, not the full image

    if thumb:
        if title:
            content += '  <div class="thumbcaption">'
            if magnify and not file_not_found:
                href = urllib.parse.quote(options["link"])
                content_magnify = f'<a href="{href}" class="internal" title="Enlarge">🔍</a>'
                content += f'<div class="magnify">{content_magnify}</div>'
            content += f"{title}</div>\n"

        style = ""
        if options["width"]:
            style = f'width: {options["width"] + 2}px;'

        if style:
            style = f' style="{style}"'

        content = f'<div class="thumbinner"{style}>{content}</div>'
        if options["horizontal"] == "center":
            content = f'<div class="thumb tnone">{content}</div>'
            content = f'<div class="{options["horizontal"]}">{content}</div>'
        else:
            content = f'<div class="thumb t{options["horizontal"]}">{content}</div>'
    else:
        if options["horizontal"]:
            if options["horizontal"] == "center":
                content = f'<div class="floatnone">{content}</div>'
                content = f'<div class="{options["horizontal"]}">{content}</div>'
            else:
                content = f'<div class="float{options["horizontal"]}">{content}</div>'

    wikilink.string = content
    return True
