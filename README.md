# JioSaavnPy

JioSaavnPy is a tool to download songs from JioSaavn.

## Supports

- Downloading by song name
- Downloading by song URL
- Donwloading by playlist URL
- Downloading by album URL

## Installation

- Clone the repo and move to the folder

```
git clone https://github.com/deepjyoti30/jiosaavnpy && cd jiosaavnpy
```

- Install using the following command

```
sudo python setup.py install
```

## Usage

- Download a song by name: 

```
jiosaavnpy <song-name>
```

Above command searches the song-name in JioSaavn and prompts the user to make a choice.
The choosen option is then downloaded.

- Download a song by URL:

```
jiosaavnpy https://www.jiosaavn.com/song/one-kiss/NiBSVSV5WV8
```

Above command downloads the song [One Kiss](https://www.jiosaavn.com/song/one-kiss/NiBSVSV5WV8)

- Download a playlist:

```
jiosaavnpy https://www.jiosaavn.com/featured/top-jiotunes---hindi/AZNZNH1EwNjfemJ68FuXsA__
```

Above command downloads the playlist [Top Jiotunes Hindi](https://www.jiosaavn.com/featured/top-jiotunes---hindi/AZNZNH1EwNjfemJ68FuXsA__)

- Download an album:

```
jiosaavnpy https://www.jiosaavn.com/album/x-wembley-edition/OIvKmsM7Tk8_
```

Above command downloads the album [x (Webley Edition)](https://www.jiosaavn.com/album/x-wembley-edition/OIvKmsM7Tk8_).


### Default Folder

- Songs are saved to the ```~/Music/``` folder.

- Playlists are saved to ```~/Music/<playlist-name>``` folder.

- Albums are saved to ```~/Music/<album-name>``` folder.

### How it Works

It basically scraps the JioSaavn pages to get the meta info of playlists, albums, songs passed.

The download URL of the song is extracted by [drt420](https://github.com/drt420)'s script that is linked
in the [Credits](#Credits) section.

## Credits

Uses [Saavn-Downloader](https://github.com/drt420/Saavn-Downloader) by [drt420](https://github.com/drt420) to extract the download URL of the song.