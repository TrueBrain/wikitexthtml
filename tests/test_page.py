from wikitexthtml import Page


def test_page_not_found():
    class PageTest(Page):
        def page_exists(self, page: str) -> bool:
            return False

    assert PageTest("Test").render().html == "<h2>Page Test not found</h2>"
