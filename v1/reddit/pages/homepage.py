from reddit.pages.utils.static_page import StaticPage


class Homepage(StaticPage):

    def _get_url(self):
        return "https://www.reddit.com/"

    def _get_next_sig(self):
        return "data.home.elements.edges"
