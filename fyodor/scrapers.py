import requests
import urllib.request
import time
import discord
from bs4 import BeautifulSoup


class WikipediaScraper(object):

    def __init__(self):
        self.url = "https://en.wikipedia.org/wiki/Portal:Current_events"


    def get_headlines(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.select("div")
        headlines_div = list(filter(lambda div: div.get("aria-labelledby") == "Topics_in_the_news", divs))
        if len(headlines_div) == 0:
            return []

        headline_div = headlines_div[0]
        headlines_ul = headline_div.select("ul")
        if len(headlines_ul) == 0:
            return []

        headlines_ul = headlines_ul[0]
        headlines = headlines_ul.select("li")
        headline_dicts = []
        for headline in headlines:
            anchor = None
            anchors = headline.select("a")
            if len(anchors) > 0:
                anchor = anchors[0]
            headline_dicts.append({
                "title": headline.text,
                "summary": headline.text,
                "url": anchor.get("href")
            })

        return headline_dicts


class CNBCScraper(object):

    def __init__(self):
        self.url = "https://www.cnbc.com/"


    def get_headlines(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.select("div")
        headlines_divs = list(filter(lambda div: "LatestNews-headline" in div.get("class", []), divs))
        if len(headlines_divs) == 0:
            return []

        headline_dicts = []
        for headline_div in headlines_divs:
            anchor_url = None
            anchors = headline_div.select("a")
            if len(anchors) > 0:
                anchor_url = anchors[0].get("href")
            headline_dicts.append({
                "title": headline_div.text,
                "summary": headline_div.text,
                "url": anchor_url
            })

        return headline_dicts


if __name__ == "__main__":
    # wikipedia_scraper = WikipediaScraper()
    # wikipedia_scraper.get_headlines()
    cnbc_scraper = CNBCScraper()
    cnbc_scraper.get_headlines()
