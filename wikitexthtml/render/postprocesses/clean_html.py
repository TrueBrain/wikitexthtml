import regex

from .helper import ChainHTMLParser
from ..config import (
    ATTRIBUTE_TO_STYLE,
    VALID_TAGS,
)


class HTMLParser(ChainHTMLParser):
    def construct_tag(self, tag, attrs):
        result = f"{tag}"

        attrs = dict(attrs)

        # Convert some old-skool HTML tags to modern HTML tags
        if tag in ("table", "td", "th", "br"):
            style = ""
            for key, replace_key in ATTRIBUTE_TO_STYLE.items():
                if key in attrs:
                    # XXX - Mediawiki doesn't allow height tags on tables
                    if key == "height" and tag == "table":
                        del attrs[key]
                        continue

                    if key == "nowrap":
                        value = key
                    else:
                        value = attrs[key].strip()

                    if key == "clear" and value == "all":
                        value = "both"

                    if key in ("height", "width") and value.isnumeric():
                        value = f"{value}px"

                    style += f"{replace_key}: {value}; "
                    del attrs[key]

            if style:
                attrs["style"] = f"{style}{attrs.get('style', '').strip()}"

        for key, value in attrs.items():
            if value is None:
                result += f" {key}"
            elif value.strip() == "":
                # Do not output empty tags
                pass
            else:
                if key == "style":
                    # Remove double spaces from any entry
                    value = regex.sub(r" \s+", r" ", value)

                value = value.strip()
                value = value.replace('"', "&quot;").replace("  ", " ")

                result += f' {key}="{value}"'

        return result

    def handle_starttag(self, tag, attrs):
        if tag not in VALID_TAGS:
            self._result += self._html_escape(self.get_starttag_text())
        elif tag == "br":
            # Replace <br> with <br/>
            self._result += "<" + self.construct_tag(tag, attrs) + " />"
        else:
            self._result += "<" + self.construct_tag(tag, attrs) + ">"

    def handle_startendtag(self, tag, attrs):
        if tag not in VALID_TAGS:
            self._result += self._html_escape(self.get_starttag_text())
        else:
            self._result += "<" + self.construct_tag(tag, attrs) + " />"

    def handle_endtag(self, tag):
        if tag not in VALID_TAGS:
            self._result += self._html_escape(self.get_endtag_text(tag))
        else:
            self._result += f"</{tag}>"

    def handle_data(self, data):
        self._result += data.replace("<", "&lt;").replace(">", "&gt;")
