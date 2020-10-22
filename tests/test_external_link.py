from wikitexthtml import Page


def test_external_link_with_title():
    class PageTest(Page):
        def page_load(self, page: str) -> str:
            return "[https://www.example.com Example]"

        def page_exists(self, page: str) -> bool:
            return True

    assert PageTest("Test").render().html == '<a class="external" href="https://www.example.com">Example</a>'


def test_external_link_without_title():
    class PageTest(Page):
        def page_load(self, page: str) -> str:
            return "[https://www.example.com]"

        def page_exists(self, page: str) -> bool:
            return True

    assert PageTest("Test").render().html == '<a class="external" href="https://www.example.com">[1]</a>'
