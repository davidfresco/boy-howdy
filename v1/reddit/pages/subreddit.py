from reddit.pages.utils.static_page import StaticPage


class Subreddit(StaticPage):

    def __init__(self, driver, sub_name):
        self.sub_name = sub_name
        StaticPage.__init__(self, driver)

    def _get_url(self):
        return f"https://www.reddit.com/r/{self.sub_name}/"

    def _get_next_sig(self):
        return "data.subredditInfoByName.elements.edges"
