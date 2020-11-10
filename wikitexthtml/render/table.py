import html
import wikitextparser

from . import list_
from ..prototype import WikiTextHtml


def _render_table(instance: WikiTextHtml, table: wikitextparser.Table):
    table_style = ""
    table_extra = ""
    for attr, value in table.attrs.items():
        if attr == "style":
            style = html.escape(value, quote=False).replace('"', "'").strip()
            if not style:
                instance.add_error(f'Table attribute "{attr}" has an empty value, which was not expected.')
            elif not style.endswith(";"):
                style += ";"
            table_style += f"{style} "
        elif attr in (
            "align",
            "bgcolor",
            "border",
            "cellpadding",
            "cellspacing",
            "class",
            "rules",
            "width",
        ):
            value = html.escape(value).strip()
            if not value:
                instance.add_error(f'Table attribute "{attr}" has an empty value, which was not expected.')
            else:
                table_extra += f' {attr}="{value}"'
        elif attr in ("bordercolor", "padding"):
            # Nobody likes these attributes; just ignore it
            pass
        else:
            instance.add_error(f'Table attribute "{attr}" is not a valid attribute.')

    if table_style:
        table_style = f' style="{table_style[:-1]}"'

    content = f"<table{table_extra}{table_style}>\n"
    if table.caption:
        caption_attrs = ""
        if table.caption_attrs:
            caption_attrs = f" {table.caption_attrs.strip()}"
        content += f"<caption{caption_attrs}>{table.caption}\n</caption>\n"

    content += "<tbody>\n"

    for row in table.cells(span=False):
        content += "<tr>\n"
        for cell in row:
            if cell is None:
                continue

            cell_style = ""
            cell_extra = ""

            for attr, value in cell.attrs.items():
                if attr == "style":
                    style = html.escape(value, quote=False).replace('"', "'").strip()
                    if not style:
                        instance.add_error(f'Cell attribute "{attr}" has an empty value, which was not expected.')
                    elif not style.endswith(";"):
                        style += ";"
                    cell_style += f"{style} "
                elif attr in ("align", "bgcolor", "class", "colspan", "height", "rowspan", "scope", "valign", "width"):
                    value = html.escape(value).strip()
                    if not value:
                        instance.add_error(f'Cell attribute "{attr}" has an empty value, which was not expected.')
                    else:
                        cell_extra += f' {attr}="{value}"'
                elif attr in ("nowrap",):
                    cell_extra += f" {attr}"
                else:
                    instance.add_error(f'Cell attribute "{attr}" is not a valid attribute.')

            if cell_style:
                cell_style = f' style="{cell_style[:-1]}"'

            if cell.is_header:
                tag = "th"
            else:
                tag = "td"

            content += f"<{tag}{cell_extra}{cell_style}>\n"
            if "\n" in cell.value:
                content += cell.value
            else:
                content += cell.value.strip()
            content += f"\n</{tag}>\n"
        content += "</tr>\n"

    content += "</tbody>\n"
    content += "</table>\n"

    index = instance.store_snippet(content)
    table.string = "{{" + f"__snippet|wikilink|{index}|table" + "}}"


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for table in reversed(wikitext.get_tables(recursive=True)):
        # Resolve all lists inside the table next
        list_.replace(instance, table)

        # Now render the table and replace it with a marker
        _render_table(instance, table)
