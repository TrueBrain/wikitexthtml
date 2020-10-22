from wikitexthtml import Page


def test_comment():
    class PageTest(Page):
        def page_load(self, page: str) -> str:
            return "Header<!-- comment -->Footer"

        def page_exists(self, page: str) -> bool:
            return True

    assert PageTest("Test").render().html == "<p>HeaderFooter</p>"
