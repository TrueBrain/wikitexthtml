import logging
import wikitextparser

from ...prototype import WikiTextHtml

log = logging.getLogger(__name__)


def hook(instance: WikiTextHtml, tag: wikitextparser.Tag):
    caption = None
    perrow = None
    heights = None
    widths = 120

    for attr, value in tag.attrs.items():
        if attr in ("heights", "widths"):
            if value.endswith("px"):
                value = value[:-2]
            if not value.isnumeric():
                raise NotImplementedError(f"Gallery attribute {attr} is not in pixels: {value}")
            if attr == "widths":
                widths = int(value)
            else:
                heights = int(value)
        elif attr == "perrow":
            if not value.isnumeric():
                raise NotImplementedError(f"Gallery attribute perrow is not a number: {value}")
            perrow = int(value)
        elif attr == "caption":
            caption = value
        elif attr == "mode":
            if value != "traditional":
                raise NotImplementedError(f"Gallery attribute mode has on traditional implemented; requested: {value}")
        else:
            raise NotImplementedError(f"Gallery attribute {attr} not yet implemented")

    if perrow:
        max_width = perrow * (widths + 43)
        content = f'<ul class="gallery" style="max-width: {max_width}px;">\n'
    else:
        content = '<ul class="gallery">\n'
    if caption:
        content += f'<li class="gallerycaption">{caption}</li>\n'

    if heights is None:
        heights = widths

    items = tag.contents.split("\n")
    for item in items:
        if not item:
            continue

        image, _, title = item.partition("|")
        if not image.lower().startswith("file:"):
            log.error(f"Unsupported entry in gallery tag: {image}")
            continue
        image = image[5:]
        url = image

        content_item = f'<img src="/uploads/{url}" style="max-width: {widths}px; max-height: {heights}px;" />\n'
        content_item = f'<a href="/File:{image}">\n{content_item}</a>\n'
        content_item = f'<div style="margin: 10px auto;">\n{content_item}</div>\n'

        style = f'style="width: {widths + 30}px; height: {heights + 30}px;"'
        content_item = f'<div class="thumb" {style}>\n{content_item}</div>\n'

        content_item += f'<div class="gallerytext">{title}</div>\n'

        content_item = f'<div style="width: {widths + 35}px">\n{content_item}</div>\n'
        content += f'<li class="gallerybox" style="width: {widths + 35}px;">\n{content_item}</li>\n'

    content += "</ul>\n"
    return content
