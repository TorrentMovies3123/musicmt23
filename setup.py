from setuptools import setup

setup(
    name="JioSaavnpy",
    packages=[
                'jiosaavnpy',
                'jiosaavnpy.saavn',
                'jiosaavnpy.song',
                'jiosaavnpy.playlist',
                'jiosaavnpy.downloader',
                'jiosaavnpy.album'
             ],
    author='deepjyoti30',
    author_email="deep.barman30@gmail.com",
    description="Download songs from JioSaavn with metadat",
    long_description="",
    url='https://github.com/deepjyoti30/jiosaavnpy',
    entry_points={
        'console_scripts': [
            'jiosaavnpy = jiosaavnpy.main:main'
        ]
    },
    version='2019.20.02',
    install_requires=['requests', 'lxml', 'beautifulsoup4', ]
)