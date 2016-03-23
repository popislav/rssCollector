import re
import feedparser


class MyParser:
    url = ""
    posts = []

    def __init__(self, url):
        self.url = url
        self.posts = []

    def parse(self):
        feed_items = feedparser.parse(self.url)
        # check
        # for item in feed_items:
        #     print(feed_items[item])
        for entry in feed_items['entries']:
            post = {}
            post['title'] = self.__find_title__(entry)
            post['link'] = self.__find_link__(entry)
            post['author'] = self.__find_author__(entry)
            post['published'] = self.__find_published__(entry)
            post['img'] = self.__find_img__(entry)
            self.posts.append(post)

    def get_posts(self):
        return self.posts

    @staticmethod
    def __find_title__(entry):
        try:
            return entry.title
        except:
            return ""


    @staticmethod
    def __find_link__(entry):
        try:
            return entry.link
        except:
            return ""

    @staticmethod
    def __find_author__(entry):
        try:
            return entry.author
        except:
            return ""

    @staticmethod
    def __find_published__(entry):
        try:
            return entry.published
        except:
            return ""

    @staticmethod
    def __find_img__(entry):
        try:
            entry['summary_detail']['value']
            pattern = re.compile('http(.+?)"')
            img_src = pattern.search(entry['summary_detail']['value'])
            try:
                # print(img_src.group()[:-1])
                return img_src.group(0)[:-1]
            except:
                return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
        except:
            return ""



    # def get_title(self):
    #     return self.title
    #
    # def get_link(self):
    #     return self.link
    #
    # def get_author(self):
    #     return self.author
    #
    # def get_published_date(self):
    #     return self.published_date
    #
    # def get_img_src(self):
    #     return self.img_scr




