from typing import Optional


class WikiTextHtml:
    page = None  # type: Optional[str]

    def page_load(self, page: str) -> str:
        """Load the page indicated by "page" and return its body."""
        raise NotImplementedError

    def page_exists(self, page: str) -> bool:
        """Return True if and only if the page exists."""
        raise NotImplementedError

    def template_load(self, template: str) -> str:
        """Load the template indicated by "template" and return its body."""
        raise NotImplementedError

    def template_exists(self, template: str) -> bool:
        """Return True if and only if the template exists."""
        raise NotImplementedError

    def file_exists(self, file: str) -> bool:
        """Return True if and only if the file (upload) exists."""
        raise NotImplementedError

    def clean_url(self, url: str) -> str:
        """Clean "url" (which is a wikilink) to become a valid URL to call."""
        raise NotImplementedError

    def clean_title(self, title: str) -> str:
        """Clean "title" (which is a full pagename) to become more human readable."""
        raise NotImplementedError

    def file_get_link(self, url: str) -> str:
        """Get the link to a file (for the "a href" of the File)."""
        raise NotImplementedError

    def file_get_img(self, url: str, thumb: Optional[int] = None) -> str:
        """Get the "img src" to a file. If thumb is set, a thumb should be generated of that size."""
        raise NotImplementedError
