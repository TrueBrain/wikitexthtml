from wikitexthtml import Page


def test_bold_and_italic():
    class PageTest(Page):
        def page_load(self, page: str) -> str:
            return "''i'' - '''b''' - '''''ib'''''"

        def page_exists(self, page: str) -> bool:
            return True

    assert PageTest("Test").render().html == "<p><i>i</i> - <b>b</b> - <i><b>ib</b></i></p>"


def test_overlapping_bold_and_italic():
    class PageTest(Page):
        def page_load(self, page: str) -> str:
            return "''a''' ''b'' zz'''c''"

        def page_exists(self, page: str) -> bool:
            return True

    assert PageTest("Test").render().html == "<i>a<b></i>b<i>zz</b>c</i>"
