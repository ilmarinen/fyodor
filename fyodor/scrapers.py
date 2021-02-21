import requests
import urllib.request
import time
import discord
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def get_first_anchor_url(bs_element):
    anchor_url = None
    anchors = bs_element.select("a")
    if len(anchors) > 0:
        anchor_url = anchors[0].get("href")

    return anchor_url


class WikipediaScraper(object):

    name = "Wikipedia"

    def __init__(self):
        self.url = "https://en.wikipedia.org/wiki/Portal:Current_events"


    def get_headlines(self, **kwargs):
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

    name = "CNBC"

    def __init__(self):
        self.url = "https://www.cnbc.com/"


    def get_headlines(self, **kwargs):
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


class EkantipurScraper(object):

    name = "Ekantipur"

    def __init__(self):
        self.url = "https://ekantipur.com/"


    def get_headlines(self, **kwargs):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        sections = soup.select("section")
        headline_sections = list(filter(lambda section: "listLayout" in section.get("class", []), sections))
        if len(headline_sections) == 0:
            return []

        headline_section = headline_sections[0]
        headline_articles = headline_section.select("article")

        headline_dicts = []
        for headline_article in headline_articles:
            anchor_url = None
            anchors = headline_article.select("a")
            if len(anchors) > 0:
                anchor_url = anchors[0].get("href")
            headline_dicts.append({
                "title": headline_article.text,
                "summary": headline_article.text,
                "url": anchor_url
            })

        return headline_dicts


class VzgalyadScraper(object):

    name = "Vzglyad"

    def __init__(self):
        self.url = "https://vz.ru/"
        model_name = 'Helsinki-NLP/opus-mt-ru-en'
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def translate_to_en(self, text_lines_ru):
        src_text_lines = []
        for text_line_ru in text_lines_ru:
            src_text = f">>en<< {text_lines_ru}"
            src_text_lines.append(src_text)
        tokenized_translated = self.model.generate(**self.tokenizer.prepare_seq2seq_batch(src_text_lines, return_tensors="pt"))
        translated_lines = [self.tokenizer.decode(t, skip_special_tokens=True) for t in tokenized_translated]

        return translated_lines

    def get_headlines(self, translate_to_en=False):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.select("div")
        mainnews_divs = list(filter(lambda d: "mainnews" in d.get("class", []), divs))
        othernews_divs = list(filter(lambda d: "othnews" in d.get("class", []), divs))
        if len(mainnews_divs) == 0 and len(othernews_divs) == 0:
            return []

        headline_texts = []
        anchor_urls = []
        for mainnews_div in mainnews_divs:
            anchor_url = get_first_anchor_url(mainnews_div)
            headline_text = mainnews_div.select("h1")[0].text.strip()
            if translate_to_en:
                headline_text = self.translate_to_en([headline_text])[0]
            if headline_text.find("------------------") == -1:
                headline_texts.append(headline_text)
                anchor_urls.append(anchor_url)

        for othernews_div in othernews_divs:
            anchor_url = get_first_anchor_url(othernews_div)
            headline_text = othernews_div.select("h4")[0].text.strip()
            if translate_to_en:
                headline_text = self.translate_to_en([headline_text])[0]
            if headline_text.find("------------------") == -1:
                headline_texts.append(headline_text)
                anchor_urls.append(anchor_url)

        headline_dicts = []
        print(headline_texts)
        for headline_text, anchor_url in zip(headline_texts, anchor_urls):
            headline_dicts.append({
                "title": headline_text,
                "summary": headline_text,
                "url": anchor_url
            })

        return headline_dicts
