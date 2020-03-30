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

# Open TSV file
# https://datasets.imdbws.com/title.basics.tsv.gz and https://datasets.imdbws.com/title.ratings.tsv.gz
with open("ratings.csv", "r") as ratings:

    ratings_reader = csv.DictReader(ratings, delimiter="\t")

    # Iterate over TSV file
    for row in ratings_reader:

        ratings_id = int(row["tconst"][2:])
        averageRating = float(row["averageRating"])
        numVotes = float(row["numVotes"])

    	# Check if the movie from the ratings tsv is in the shows tsv
        show_row = db.execute("SELECT * FROM shows WHERE id=:ratings_id", {"ratings_id": ratings_id}).fetchone()

    	# If the movie exists in both the ratings AND shows tsv
        if show_row is not None:
            # print(show_row)

            # If rating is higher than 6.5
            if float(row["averageRating"]) > 6.5:

                # Update rating column in shows database
                db.execute("UPDATE shows SET rating = :rating, numVotes = :numVotes WHERE id = :id", {"rating": averageRating, "numVotes": numVotes, "id": ratings_id})

                # Save (and commit) changes
                db.commit()
            
            # If rating is below 6.5
            else:

                # Remove row with that id from genres and shows databases
                db.execute("DELETE FROM genres WHERE show_id = :id", {"id": ratings_id})
                db.execute("DELETE FROM shows WHERE id = :id", {"id": ratings_id})

                # Save (and commit) changes
                db.commit()	

exit(0)