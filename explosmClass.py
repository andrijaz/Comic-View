import requests, re,  sys

latest_url = "http://explosm.net/comics/latest"
base_url = "http://explosm.net/comics/"

def find_latest():
    pattern_link = r"<input\s*id=\"permalink\".*\s*value=.*\/([0-9]+)"
    pattern = re.compile(pattern_link)
    string = str(requests.get(latest_url).text)
    result = re.search(pattern, string)
    return result.group(1)
def find_next(comic):
    pattern_link = r"<a\s*href=\"\/comics\/([0-9]+)\/\"\s*class=\"next-comic\s*\""
    pattern = re.compile(pattern_link)
    string = requests.get(base_url+str(comic)).text
    result = re.search(pattern, string)
    return result.group(1)
def find_prev(comic):
    #<a href="/comics/4860/" class="previous-comic "
    pattern_link = r"<a\s*href=\"\/comics\/([0-9]+)\/\"\s*class=\"previous-comic\s*\""
    pattern = re.compile(pattern_link)
    string = requests.get(base_url+str(comic)).text
    result = re.search(pattern, string)
    return result.group(1)
class Comic():
    def __init__(self, comic_id):
        self.comic_id = comic_id
        self.permalink = "http://explosm.net/comics/"+str(self.comic_id)+"/"
        self.source = str(requests.get(self.permalink).text)
        self.img_link = ""
        self.title = ""
        self.author = ""
        self.date = {}
        self.comments = 0
        self.stars = 0
        self.next = 0
        self.previous = 0
    def __str__(self):
        return "{} <- {} -> {}".format(self.previous, self.comic_id, self.next)
    def get_img_link(self):
        #<img id="main-comic" src="//files.explosm.net/comics/Dave/docdrugz.png?t=891833" />
        pattern_link = r"<img\s*id=\"main-comic\"\s*src=\"(.*)\"\s*\/>"
        pattern = re.compile(pattern_link)
        string = self.source
        result = re.search(pattern, string)
        final_link = "http:"+ result.group(1)

        pattern_img_name = r"\/([a-zA-Z0-9\s-]*\.[a-z]+)\?"
        pattern = re.compile(pattern_img_name)
        result = re.search(pattern, final_link)
        final_name = result.group(1)

        self.title = final_name
        self.img_link = final_link
    def get_stats(self):
        #<span class="count">16</span>
        pattern_link = r"<span\s*class=\"count\">([0-9]*)<\/span>"
        pattern = re.compile(pattern_link)
        string = self.source
        result = re.search(pattern, string)
        stars = result.group(1)


        #<span class="comment-count">101</a>
        pattern_link = r"<span\s*class=\"comment-count\">([0-9]*)<\/a>"
        pattern = re.compile(pattern_link)
        string = self.source
        result = re.search(pattern, string)
        comments = result.group(1)
        self.comments = comments
        self.stars = stars
    def get_author(self):
        #<small class="author-credit-name">by Dave McElfatrick</small>
        pattern_link = r"<small\s*class=\"author-credit-name\">\s*by\s*([a-zA-Z\s]*)<\/small>"
        pattern = re.compile(pattern_link)
        string = self.source
        result = re.search(pattern, string)
        author = result.group(1)
        self.author = author
    def get_date(self):
        #<a href="/comics/archive/2018/02/dave ">2018.02.24</a>
        pattern_link = r"<a\s*href=\"\/comics\/archive\/.*?\s*\">([0-9]{4})\.([0-9]{2})\.([0-9]{2})<\/a>"
        pattern = re.compile(pattern_link)
        string = self.source
        result = re.search(pattern, string)
        year = result.group(1)
        month = result.group(2)
        day = result.group(3)
        self.date = {'year':year, 'month':month, 'day': day}
    def get_prev_and_next(self):
        pattern_link = r"<a\s*href=\"\/comics\/([0-9]+)\/\"\s*class=\"previous-comic\s*\""
        pattern = re.compile(pattern_link)
        string = self.source

        result = re.search(pattern, string)
        if result == None:
            self.previous = -1
        else:
            self.previous = result.group(1)

        pattern_link = r"<a\s*href=\"\/comics\/([0-9]+)\/\"\s*class=\"next-comic\s*\""
        pattern = re.compile(pattern_link)
        string = self.source
        result = re.search(pattern, string)
        if result == None:
            self.next == -1
        else:
            self.next =  result.group(1)
    def download_img(self):
        img_data = requests.get(self.img_link).content
        with open(self.title, 'wb') as handler:
            handler.write(img_data)
    def get_all_data(self):
        self.get_img_link()
        self.get_stats()
        self.get_author()
        self.get_date()
        self.get_prev_and_next()

latest_id = find_latest()
starting_comic = Comic(latest_id)
starting_comic.get_all_data()
