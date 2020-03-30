import os
import cs50
import csv
import urllib.parse
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

# Configure database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Create table 'shows'
db.execute("DROP TABLE if exists shows CASCADE")
db.execute("CREATE TABLE shows (id INT PRIMARY KEY, title TEXT, year NUMERIC, rating REAL, numVotes INTEGER, ranking REAL)")

# The `genres` table will have a column called `show_id` that references the `shows` table above
db.execute("DROP TABLE if exists genres CASCADE")
db.execute("CREATE TABLE genres (show_id INT, genre TEXT, FOREIGN KEY(show_id) REFERENCES shows(id) ON DELETE CASCADE)")

# Create test table 'ratings'
db.execute("DROP TABLE if exists ratings CASCADE")
# db.execute("CREATE TABLE ratings (id INT PRIMARY KEY, averageRating REAL, numVotes INTEGER)")


# Open TSV file
# https://datasets.imdbws.com/title.basics.tsv.gz and https://datasets.imdbws.com/title.ratings.tsv.gz
with open("title.basics.tsv", "r") as titles, open("title.ratings.tsv", "r") as ratings:

    # Create DictReaders
    reader = csv.DictReader(titles, delimiter="\t")
    ratings_reader = csv.DictReader(ratings, delimiter="\t")

    # Iterate over TSV file
    for row in reader:

        # If non-adult TV show
        if row["titleType"] == "movie" and row["isAdult"] == "0":

            # If year not missing
            if row["startYear"] != "\\N":

            	# If since 1970
                startYear = int(row["startYear"])
                if startYear >= 1970:

	                # Trim prefix from tconst
	                id = int(row["tconst"][2:])

	                # Insert show
	                db.execute("INSERT INTO shows (id, title, year) VALUES(:id, :title, :year)", {"id": id, "title": row["primaryTitle"], "year": startYear})

	                # Insert genres
	                if row["genres"] != "\\N":
	                    
	                    for genre in row["genres"].split(","):
	                        db.execute("INSERT INTO genres (show_id, genre) VALUES(:id, :genre)", {"id": id, "genre": genre})

                        # Save (and commit) changes    
	                    db.commit()

    # Iterate over TSV file
    for row in ratings_reader:

        ratings_id = int(row["tconst"][2:])
        averageRating = float(row["averageRating"])
        numVotes = int(row["numVotes"])

    	# Check if the movie from the ratings tsv is in the shows tsv
        show_row = db.execute("SELECT * FROM shows WHERE id=:ratings_id", {"ratings_id": ratings_id}).fetchone()

    	# If the movie exists in both the ratings AND shows tsv
        if show_row is not None:

            # If rating is higher than 6.5
            if float(row["averageRating"]) > 6.5:

            	# Update rating column in shows database
            	db.execute("UPDATE shows SET rating = :rating, numVotes = :numVotes WHERE id = :id", {"rating": averageRating, "numVotes": numVotes, "id": ratings_id})
            
            # If rating is below 6.5
            else:

                # Remove row with that id from genres and shows databases
                db.execute("DELETE FROM genres WHERE show_id = :id", {"id": ratings_id})
                db.execute("DELETE FROM shows WHERE id = :id", {"id": ratings_id})	

    # Delete all movies that exist in shows database, but not in ratings database
    db.execute("DELETE from shows WHERE rating IS NULL")

    # Save (and commit) changes
    db.commit()

    # Add the IMDB ranking to shows https://help.imdb.com/article/imdb/track-movies-tv/ratings-faq/G67Y87TFYYP6TWAV#included
    db.execute("UPDATE shows SET ranking = :ranking", {"ranking": ((numVotes / (numVotes + 25000)) * averageRating) + ((25000 / (numVotes + 25000)) * AVG(averageRating))})

    # Save (and commit) changes
    db.commit()

exit(0)