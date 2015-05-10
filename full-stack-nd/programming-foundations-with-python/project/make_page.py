#! /usr/bin/env python

""" top-level executable """

import webbrowser
import sys

from movie_data import movies
from format_html import write_movies_page

path_page = write_movies_page(movies)
if '-n' not in sys.argv:
    webbrowser.open(
        'file://' + path_page,
        new=2)
