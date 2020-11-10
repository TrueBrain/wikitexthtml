import urllib
import wikitextparser

from ...prototype import WikiTextHtml


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
                instance.add_error(f'Gallery attribute "{attr}" is not in pixels: {value}.')
            if attr == "widths":
                widths = int(value)
            else:
                heights = int(value)
        elif attr == "perrow":
            if not value.isnumeric():
                instance.add_error(f'Gallery attribute "{attr}" is not in a number: {value}.')
            perrow = int(value)
        elif attr == "caption":
            caption = value
        elif attr == "mode":
            if value != "traditional":
                instance.add_error(f'Gallery attribute "{attr}" has an unsupported value: {value}.')
        else:
            instance.add_error(f'Gallery attribute "{attr}" is not a valid attribute.')

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
            instance.add_error(f'Gallery entry "{image}" is not a valid gallery entry.')
            continue
        image = image[5:]

        url = instance.file_get_link(image)
        url = urllib.parse.quote(url)

        img = instance.file_get_img(image)
        img = urllib.parse.quote(img)

        content_item = f'<img src="{img}" style="max-width: {widths}px; max-height: {heights}px;" />\n'
        content_item = f'<a href="{url}">\n{content_item}</a>\n'
        content_item = f'<div style="margin: 10px auto;">\n{content_item}</div>\n'

        style = f'style="width: {widths + 30}px; height: {heights + 30}px;"'
        content_item = f'<div class="thumb" {style}>\n{content_item}</div>\n'

        content_item += f'<div class="gallerytext">{title}</div>\n'

        content_item = f'<div style="width: {widths + 35}px">\n{content_item}</div>\n'
        content += f'<li class="gallerybox" style="width: {widths + 35}px;">\n{content_item}</li>\n'

    content += "</ul>\n"
    return content
