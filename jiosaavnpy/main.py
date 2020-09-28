"""Main function and other subfunctions defined."""

import argparse

from jiosaavnpy.song.song import Song
from jiosaavnpy.saavn.utility import JioSaavnURL
from jiosaavnpy.playlist.playlist import JioSaavnPlaylist
from jiosaavnpy.album.album import JioSaavnAlbum

from jiosaavnpy.logger import Logger

# Get the logger
logger = Logger('main')


def parse_arguments():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="Download songs,\
                                    playlists, albums from JioSaavn directly.\
                                    Check (https://github.com/deepjyoti30/jiosaavnpy)\
                                    for more details.")

    parser.add_argument('entity',
                        help="Name of the song to search / URL of a playlist\
                        /URL of a song/ URL of an album",
                        default=None, type=str, nargs="*")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    args.entity = ' '.join(args.entity)
    URLtype = JioSaavnURL(args.entity).type

    if URLtype == 'playlist':
        logger.info('Passed entity is a playlist URL')
        JioSaavnPlaylist(args.entity)
    elif URLtype == 'album':
        logger.info('Passed entity is an album')
        JioSaavnAlbum(args.entity)
    elif URLtype == 'song':
        logger.info('Passed entity is a song URL')
        Song(args.entity, 'URL')
    else:
        # Its a song
        logger.info('Passed entity is a Song name')
        Song(args.entity, 'name')
