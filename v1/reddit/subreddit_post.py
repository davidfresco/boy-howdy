

class Post:

    important_info = ["id", "title", "author", "subreddit", "created_at",
                      "permalink", "is_ad", "is_nsfw", "is_saved",
                      "is_stickied", "score", "upvote_ratio", "media",
                      "thumbnail", "content_link", "flair", "post_type"]

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.id = kwargs["id"]
        self.title = kwargs["title"]
        self.author = kwargs["author"]
        self.subreddit = kwargs["subreddit"]
        self.created_at = kwargs["created_at"]
        self.permalink = kwargs["permalink"]
        self.is_ad = kwargs["is_ad"]
        self.is_nsfw = kwargs["is_nsfw"]
        self.is_saved = kwargs["is_saved"]
        self.is_stickied = kwargs["is_stickied"]
        self.score = kwargs["score"]
        self.upvote_ratio = kwargs["upvote_ratio"]
        self.media = kwargs["media"]
        self.thumbnail = kwargs["thumbnail"]
        self.content_link = kwargs["content_link"]
        self.flair = kwargs["flair"]
        self.post_type = kwargs["post_type"]

    def as_json(self):
        return self.kwargs
