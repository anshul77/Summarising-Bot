import requests as _req
import wikipedia as _wk
from re import findall as _findall
from bs4 import BeautifulSoup as bs
from summarizer import FrequencySummarizer as fs

_guardian_key = "f26b6c0c-379f-4961-a47f-1dfaf40b9aa2"
_nyt_key = "02bcc44cbbf544b5927be9b458490c6f"
#_guardian_url = "http://content.guardianapis.com/search"
_guardian_url = "http://content.guardianapis.com/search?api-key=f26b6c0c-379f-4961-a47f-1dfaf40b9aa2"
_nyt_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"


class MediaAggregatorMixin:
    def __init__(self):
        #print "inside MediaAggregatorMixin"
        pass

    def get_news(self, query):
        pass

    def get_limit(self):
        pass


class GuardianAggregator:
    def __init__(self):
        self._params = {"q": "", "api-key": _guardian_key}
        self._limit = None

    def get_news(self, query):
        #print "inside get_news of GuardianAggregator"
        self._params["q"] = str(query)
        response = _req.get(_guardian_url, params = self._params)
        return [x["webUrl"] for x in response.json()["response"]["results"] if x["type"] == "article" and
                x["sectionName"] != u"Media" and "quiz" not in x["webUrl"].lower()]

    def get_limit(self):
        #print "inside get_limit of get_limit"
        if not self._limit:
            self.get_news("test")
        return self._limit


class NYTAggregator:
    def __init__(self):
        self._params = {"q": "", "api-key": _nyt_key}

    def get_news(self, query):
        #print "inside get_news of NYTAggregator"
        self._params["q"] = str(query)
        response = _req.get(_nyt_url, params = self._params)
        return [x["web_url"] for x in response.json()["response"]["docs"] if x["type_of_material"] == "News"]

    def get_limit(self):
        return self._limit


def shorten_news(url, n = 5):
    #print "inside get_news of shorten_news"
    response = _req.get(url)
    #print response
    if not response.ok:
        return False
    page = response.content
    soup = bs(page, "lxml")
    #print "soup"
    summary = fs().summarize("\n".join([x.text for x in soup.findAll("p") if len(x.text.split()) > 1]), n)
    #print "summary"
    #print summary 
    summary.insert(0, soup.title.text)
    #print "nxjnd"
    return ' '.join(summary)

def summ_from_text(text):
    n=6
    summary = fs().summarize(text,n)
    #print "summary"
    #print summary 
    return ' '.join(summary)

def get_gkg(query):
    #print "inside get_news of get_gkg"
    try:
        s = _wk.summary(query, sentences = 5)
        for x in _findall("\(.*\)", s):
            s = s.replace(x, "")
        return s
    except _wk.DisambiguationError as e:
        return False
