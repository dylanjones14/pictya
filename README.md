# pictya

Updating readme.

This is the Pictya app, that I have developed to help you and your friends choose what film to watch.

IMDB API not available, only tsv datasets. Other movie databases with free APIs are available, but wasn't satisfied with rating systems.

IMDB datasets updated: 24/03/2020

To update, visit https://www.imdb.com/interfaces/ and download latest title.basics.tsv.gz and title.ratings.tsv.gz databases and then run python import.py in your terminal. Make sure you run 'caffeinate' in your terminal and let script run overnight to generate data tables.

Note - I have restricted dataset to movies, year > 1970, rating > 6.5 to limit rows.
