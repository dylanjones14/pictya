# pictya

Pictya helps you and your friends discover top rated films that none of you have seen before. 

Have a scroll through our list of movies and select those you have seen before to create your own watchlist. Be sure to keep this up to date when you watch new movies

Then let us know who’s watching and your genre of choice. We'll show you the highest rated movies not featured on any of your watchlists.</p>

Instructions for loading datasets >>

IMDB API not available, only tsv datasets. Other movie databases with free APIs are available, but wasn't satisfied with rating systems.

IMDB datasets updated: 24/03/2020

To update, visit https://www.imdb.com/interfaces/ and download latest title.basics.tsv.gz and title.ratings.tsv.gz databases. They are quite large databases, so you can use reduce.py to give a smaller dataset for running on your local machine.

Use import1.py, import2.py and import3.py to load the tsv files into your local database.

Note - I have restricted dataset to movies, year > 1970, rating > 6.5 to limit rows.

Instructions for getting code running on local machine >>

$ pip freeze > requirements.txt
$ sudo pip install virtualenv
$ virtualenv myenv
$ source myenv/bin/activate
$ pip install -r requirements.txt

Download the Mac App Postgres.app. Follow the directions on the homepage, including moving the app to Applications, opening it, and clicking “Initialize” to start the server. Ignore the page’s Step 3 for now.

$ PATH = "/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
$ echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
$ export DATABASE_URL="postgresql://localhost/[DB_NAME]"
$ touch .env

Inside this should be the same information as the last command in the previous step:
export DATABASE_URL="postgresql://localhost/[DB_NAME]"

$ sudo pip install psycopg2
$ python application.py

You should now be able to run this on your local machine.


