import re
import time
import json
from lxml import html

from reddit.subreddit_post import Post
from reddit.pages.utils.page import Page
from reddit.pages.utils.request_utils import get_target_request_body


class StaticPage(Page):

    def __init__(self, driver, *args, **kwargs):
        Page.__init__(self, driver)

    def _get_url(self):
        pass

    def _get_next_sig(self):
        pass

    def _get_next_edges(self, data):
        for key in self._get_next_sig().split("."):
            data = data[key]
        return [edge["node"] for edge in data]

    def _get_first_page_data(self):
        body_text = get_target_request_body(
            self._driver, url_regex=f"^{self._get_url()}$")
        data_elem = html.fromstring(body_text).xpath("//script[@id='data']")[0]
        data_text = re.match(r"window\.___r = (.*);", data_elem.text).group(1)
        data = json.loads(data_text)
        return data

    def first_page(self):
        self._driver.get(self._get_url())
        data = self._get_first_page_data()
        post_data = []
        for id in data["posts"]["models"].keys():
            post = data["posts"]["models"][id]
            post_type = post["belongsTo"]["type"]
            if post_type == "subreddit":
                sub_id = post["belongsTo"]["id"]
                sub_name = data["subreddits"]["models"][sub_id]["name"]
            else:
                sub_name = None
            try:
                post_obj = Post(
                    id=post["id"], title=post["title"], author=post["author"],
                    subreddit=sub_name, created_at=post["created"],
                    permalink=post["permalink"],
                    is_ad=post["isCreatedFromAdsUi"], is_nsfw=post["isNSFW"],
                    is_saved=post["saved"], is_stickied=post["isStickied"],
                    score=post["score"], upvote_ratio=post["upvoteRatio"],
                    media=post["media"], thumbnail=post["thumbnail"],
                    content_link=None, flair=post["flair"],
                    post_type=post_type)
            except KeyError as e:
                print(post)
                raise Exception("failed to find key: ", e.args[0])
            post_data.append(post_obj)
        return post_data

    def _get_next_page_data(self):
        while len(self.get_elems("//div[@data-testid='post-container']")) < 25:
            time.sleep(0.5)
        del self._driver.requests
        self.scroll_to_bottom()
        body_text = get_target_request_body(
            self._driver, response_sig=self._get_next_sig())
        data = json.loads(body_text)
        return data

    def next_page(self):
        data = self._get_next_page_data()
        post_data = []
        for post in self._get_next_edges(data):
            post_type = post["__typename"]
            if post_type == "PostRecommendation":
                post = post["postInfo"]
            subreddit = None if post_type == "AdPost" else post["subreddit"]
            try:
                post_obj = Post(
                    id=post["id"], title=post["title"],
                    author=post["authorInfo"], subreddit=subreddit,
                    created_at=post["createdAt"], permalink=post["permalink"],
                    is_ad=post["isCreatedFromAdsUi"], is_nsfw=post["isNsfw"],
                    is_saved=post["isSaved"], is_stickied=post["isStickied"],
                    score=post["score"], upvote_ratio=post["upvoteRatio"],
                    media=post["media"], thumbnail=post["thumbnail"],
                    content_link=None, flair=post["flair"],
                    post_type=post_type)
            except KeyError as e:
                print(f"failed to find key: '{e.args[0]}'")
                print(post)
                break
            post_data.append(post_obj)
        return post_data
