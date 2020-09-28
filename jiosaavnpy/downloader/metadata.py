"""Metadata related functions defined."""

import os
from mutagen.id3 import (
                    ID3,
                    APIC,
                    TIT2,
                    TPE1,
                    TALB,
                    TRCK,
                    TYER,
                    ID3NoHeaderError
                        )
from mutagen.mp3 import MP3

from jiosaavnpy.downloader.downloader import Download

from jiosaavnpy.logger import Logger

# Setup logger
logger = Logger('metadata')


class SetMetadata:
    """
    Set the metadata to the mp3 file downloaded.
    """

    def __init__(self, path, song_data):
        self.SONG_PATH = path
        self.song_data = song_data
        self.cover = ''
        self._checkexistence()
        self._dw_cover()
        self._set_data()

    def _checkexistence(self):
        """Check if the passed song path exists."""
        if not os.path.isfile(self.SONG_PATH):
            logger.critical("{}: does not exist".format(self.SONG_PATH))
            # exit(-1)

    def _dw_cover(self):
        """
        Download the cover from the data provided.
        """
        if self.song_data.artwork != '':
            logger.info('Downloading album artwork...')
            download_obj = Download(self.song_data.artwork, False)
            download_obj.download()
            result = download_obj.des_path
            self.cover = result if result is not False else None

    def _set_data(self):
        """Set the song data in the song."""
        IS_IMG_ADDED = False

        SONG_PATH = self.SONG_PATH

        audio = MP3(SONG_PATH, ID3=ID3)

        try:
            data = ID3(SONG_PATH)
        except ID3NoHeaderError:
            data = ID3()

        # If cover is not None then add it
        if self.cover is not None:
            if not os.path.isfile(self.cover):
                logger.warning("{}: does not exist. Skipping..".format(self.cover))
            else:
                imagedata = open(self.cover, 'rb').read()
                data.add(APIC(3, 'image/jpeg', 3, 'Front cover', imagedata))
                # REmove the image
                os.remove(self.cover)
                IS_IMG_ADDED = True

        # If tags are not present then add them
        try:
            audio.add_tags()
        except Exception:
            pass

        audio.save()

        data.add(TYER(encoding=3, text=self.song_data.releaseDate))
        data.add(TIT2(encoding=3, text=self.song_data.title))
        data.add(TPE1(encoding=3, text=self.song_data.artist))
        data.add(TALB(encoding=3, text=self.song_data.album))
        data.add(TRCK(encoding=3, text=str(self.song_data.trackNumber)))

        data.save(SONG_PATH)

        # Show the written stuff in a better format
        print('================================')
        print('  || YEAR: ' + self.song_data.releaseDate)
        print('  || TITLE: ' + self.song_data.title)
        print('  || ARITST: ' + self.song_data.artist)
        print('  || ALBUM: ' + self.song_data.album)
        print('  || TRACK NO: ' + str(self.song_data.trackNumber))

        if IS_IMG_ADDED:
            print('  || ALBUM COVER ADDED')

        print('================================')
