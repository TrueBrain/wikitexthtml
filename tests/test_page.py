from wikitexthtml import Page


def test_page_not_found():
    class PageTest(Page):
        def page_load(self, page: str) -> str:
            return "page_load() called"

        def page_exists(self, page: str) -> bool:
            return False

    assert PageTest("Test").render().html == "<p>page_load() called</p>"
