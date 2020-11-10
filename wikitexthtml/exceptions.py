class InvalidWikiLink(Exception):
    """Raised if a wikilink is invalid, indicating it should render as [[...]]."""


class InvalidTemplate(Exception):
    """Raised if a template name is invalid, indicating it should render as {{...}}."""
