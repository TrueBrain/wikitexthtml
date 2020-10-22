from typing import Optional


class WikiTextHtml:
    page = None  # type: Optional[str]

    def page_load(self, page: str) -> str:
        raise NotImplementedError

    def page_exists(self, page: str) -> bool:
        raise NotImplementedError

    def template_load(self, template: str) -> str:
        raise NotImplementedError

    def template_exists(self, template: str) -> bool:
        raise NotImplementedError

    def file_exists(self, file: str) -> bool:
        raise NotImplementedError

    def clean_url(self, url: str) -> str:
        raise NotImplementedError

    def clean_title(self, title: str) -> str:
        raise NotImplementedError

    def store_snippet(self, snippet: str) -> int:
        # Will be implemented by Page
        raise NotImplementedError
