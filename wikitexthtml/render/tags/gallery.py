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

    items = tag.contents.split("\n")
    for item in items:
        if not item:
            continue

        image, _, title = item.partition("|")
        if image.lower().startswith("image:"):
            image = f"file:{image[6:]}"
        if image.lower().startswith("file:"):
            image = image[5:]
        image = image.replace(" ", "_")
        url = image

        if heights:
            content_item = f'<img src="/uploads/{url}" height="{heights}" />\n'
        else:
            content_item = f'<img src="/uploads/{url}" />\n'
        content_item = f'<a href="/File:{image}">\n{content_item}</a>\n'
        content_item = f'<div style="margin: 10px auto;">\n{content_item}</div>\n'
        content_item = f'<div class="thumb" style="width: {widths + 30}px">\n{content_item}</div>\n'
        content_item += f'<div class="gallerytext">{title}</div>\n'

        content_item = f'<div style="width: {widths + 35}px">\n{content_item}</div>\n'
        content += f'<li class="gallerybox" style="width: {widths + 35}px">\n{content_item}</li>\n'

    content += "</ul>\n"
    return content
