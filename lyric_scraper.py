"""
Author: Anthony Galtier
Description : A simple web scraper to collect
              lyrics from AZLyrics.com
Version : 15-01-2020
"""

import requests
import re
import time
from bs4 import BeautifulSoup
from nltk.tokenize import TweetTokenizer


class AZLyricScraper:
    """
    A web scraper that collects song names and lyrics from AZLyrics.com
    """
    URL = 'http://www.azlyrics.com/'
    HTML_TAGS = ['br','div', 'i']

    def artist_page_url(self, artist):
        url = self.URL + artist[0] + '/' + artist + '.html'
        return url

    def list_songs(self, artist):
        url = self.artist_page_url(artist)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        songs = [str(song.text) for song in soup.find_all(target='_blank')]
        return songs

    def lyric_page_url(self, artist, song_name):
        song_url = re.sub(r'[^\w\s]','', song_name).replace(" ",'').lower()
        rest = 'lyrics/' + artist + '/' + song_url + '.html'
        return self.URL + rest

    def get_lyrics(self, artist, song_name):
        time.sleep(10)
        url = self.lyric_page_url(artist, song_name)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        lyrics = soup.find_all("div", limit=20)[-1]
        lyrics = ''.join(lyrics.find_all(text=True))
        tkn = TweetTokenizer()
        lyrics = tkn.tokenize(lyrics)
        lyrics = [word for word in lyrics if word not in self.HTML_TAGS]
        return " ".join(lyrics[20:])
