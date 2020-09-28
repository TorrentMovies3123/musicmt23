"""Functions related to album stuff defined."""

import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path

from jiosaavnpy.song.search import SearchJioSaavn
from jiosaavnpy.song.song import Song

from jiosaavnpy.logger import Logger

# Setup logger
logger = Logger('album')


class JioSaavnAlbum:
    """
    Class to download album from JioSaavn

    The page can be scrapped the same way song search page is done
    so SearchJioSaavn class is used. After that all the songs
    are downlaoded one by one.
    """

    def __init__(self, URL):
        self.URL = URL
        self._album_name = 'default'
        self.headers = {
                    'User-Agent': 'Mozilla/5.0 \
                                   (X11; Ubuntu; Linux x86_64; rv:49.0)\
                                   Gecko/20100101 Firefox/49.0'
                       }
        self.content_tuple = []
        self._extract_album_name()
        self._des_folder = Path('~/Music').expanduser().joinpath(self._album_name)
        self._extract_content()

    def _extract_album_name(self):
        """
        Extract the name of the album by doing some
        actions on the passed URL.
        """
        response = requests.get(self.URL, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        self._album_name = soup.find_all('h1', {'class': 'page-title'})
        self._album_name = re.sub(r'>|<', '', re.findall(r'>.*?<', str(self._album_name))[0])
        logger.info('Name: {}'.format(self._album_name))

    def _extract_content(self):
        """
        Extract the content and download them by sending to Song class.
        """
        logger.info('Extracting content')
        self.content_tuple = SearchJioSaavn(self.URL, 'URL').results

        for i in self.content_tuple:
            # Each song can be thought of as URL downloadable entity
            logger.info('Downloading {} by {}'.format(i.title, i.artist))
            Song(i.perma_url, 'URL', self._des_folder)
