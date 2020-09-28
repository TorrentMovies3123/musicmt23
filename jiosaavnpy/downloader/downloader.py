import urllib.request
import sys
import time
from os import path, popen
from pathlib import Path

from jiosaavnpy.logger import Logger

# Setup logger
logger = Logger('downloader')


class Download:
    """
    Downloader class to download the files.

    // URL //
    * Download URL of the file.
    * type = str

    // verbose //
    * Whether to show or not output.
    * type = bool
    * default = True

    // name //
    * Name to save the file with.
    * type = str
    * default = '' (If the name is found to be '',
                 then it is extracted from the URL)

    // des_folder //
    * Destination folder of the file.
    * type = str
    * default = ~/Music/
    """

    def __init__(
                self,
                URL,
                verbose=True,
                name='',
                des_folder='~/Music/'
                ):
        self.URL = URL
        self.verbose = verbose
        self.name = name
        self.des_folder = Path(des_folder).expanduser()
        self.des_path = None
        self._resolve_path_issues()

    def _get_terminal_length(self):
        """Return the length of the terminal."""
        rows, cols = popen('stty size', 'r').read().split()

        return int(cols)

    def _is_present(self, size):
        """
        Check if the file is already present.
        If it is then check if the file size is same or more
        as returned from the server, if it is, then skip 
        downloading.
        """
        try:
            logger.debug(size)
            logger.debug(self.des_path.stat().st_size)
            return True if self.des_path.stat().st_size >= size else False
        except FileNotFoundError:
            return False

    def _resolve_path_issues(self):
        """
        Resolve the path related issues with the passed desFol.

        If fatal issues arise then change it to ~/Music/
        """
        des_path = Path(self.des_folder).expanduser()

        try:
            des_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error('{}'.format(e))
            self.des_folder = Path('~/Music').expanduser()


    def download(self):
        try:
            if self.name == '':
                self.name = self.URL.split('/')[-1]
            else:
                if self.name.split('.')[-1] != 'mp3':
                    self.name = self.name + '.mp3'
            self.des_path = Path(self.des_folder).joinpath(self.name)

            u = urllib.request.urlopen(self.URL)
            meta = u.info()

            file_size = int(meta["Content-Length"])

            # Check if the file is already present.
            if self._is_present(file_size):
                logger.info('File already downloaded with proper metadata. Skipping..')
                return False

            f = open(self.des_path, 'wb')

            file_size_dl = 0
            block_sz = 8192

            # Show an info about the dw if verbose is enabled
            if self.verbose:
                logger.info('Downloading to {}'.format(self.des_folder))

            beg_time = time.time()
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)

                if self.verbose:
                    # Calculate speed
                    speed = (file_size_dl / 1024) / (time.time() - beg_time)

                    # Calculate time left
                    time_left = round(((file_size - file_size_dl) / 1024) / speed)
                    time_unit = 's'

                    # Convert to min or hours as req
                    if time_left > 3600:
                        time_left = round(time_left / 3600)
                        time_unit = 'h'
                    elif time_left > 60:
                        time_left = round(time_left / 60)
                        time_unit = 'm'

                    # Calculate percentage
                    percent = file_size_dl * 100. / file_size

                    # file_size to show
                    if file_size_dl > (1024 * 1024):
                        file_size_to_disp = file_size_dl / (1024 * 1024)
                        dw_unit = "MB's"
                    elif file_size_dl > 1024:
                        file_size_to_disp = file_size_dl / 1024
                        dw_unit = "kb's"

                    # Basename
                    basename = path.basename(self.des_path)

                    # Calculate amount of space req in between
                    length = self._get_terminal_length()

                    stuff_len = len(basename) + 13 + 17 + 7 + 26 + 5
                    space = 0

                    if stuff_len < length:
                        space = length - stuff_len
                    elif stuff_len > length:
                        basename = basename[:(length - stuff_len) - 2] + '..'

                    status = r"%s %s %0.2f %s |%d kbps| ETA: %s %s |%-20s| %3.2f%%" % (basename, space * " ", file_size_to_disp, dw_unit, speed, time_left, time_unit, "-" * int(percent / 5), percent)
                    sys.stdout.write('\r')
                    sys.stdout.write(status)
                    sys.stdout.flush()

            f.close()

            if self.verbose:
                print()
            return True
        except ConnectionError:
            print("Connection Error!")
            return False


if __name__ == "__main__":
    Download.download("http://speedtest.ftp.otenet.gr/files/test100k.db", 'nana.mkv')
