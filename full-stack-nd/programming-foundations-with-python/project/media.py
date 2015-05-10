""" Data format for movie information """

from pdb import set_trace as st

import urllib
from bs4 import BeautifulSoup

class Movie(object):
    """ A class to contain information about a movie """
    VALID_RATINGS = range(1, 6)

    def __init__(self, imdb_url, youtube_id, rating):
        """ scrape imdb.com for movie info """
        # store data
        self.youtube_id = youtube_id
        if rating not in self.VALID_RATINGS:
            raise ValueError("Invalid rating")
        self.rating = rating
        # scrape imdb
        f_imdb_page = urllib.urlopen(imdb_url)
        soup_page = BeautifulSoup(f_imdb_page.read(), 'html.parser')
        f_imdb_page.close()
        soup_overview = soup_page.find_all(
            'div', class_='title-overview')[0]
        self.poster_img_url = soup_overview.find('img')['src']
        self.title = soup_overview.find('h1').find('span').text
