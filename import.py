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
db.execute("CREATE TABLE shows (id INT PRIMARY KEY, title TEXT, year NUMERIC, rating REAL)")

# The `genres` table will have a column called `show_id` that references the `shows` table above
db.execute("DROP TABLE if exists genres CASCADE")
db.execute("CREATE TABLE genres (show_id INT, genre TEXT, FOREIGN KEY(show_id) REFERENCES shows(id))")

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

	                    db.commit()

    # Iterate over TSV file
    for row in ratings_reader:

    	ratings_id = int(row["tconst"][2:])
    	show_row = db.execute("SELECT * FROM shows WHERE id=:id", {"id": ratings_id}).fetchone()

    	if show_row is not None:

            if float(row["averageRating"]) > 6.5:

            	# Update rating column in shows database
            	db.execute("UPDATE shows SET rating = :rating WHERE id = :id", {"rating": float(row["averageRating"]), "id": ratings_id})
            	
                # Save (and commit) changes
            	db.commit()

            else:

                # Remove row with that id from genres and shows databases
                db.execute("DELETE FROM genres WHERE show_id = :id", {"id": ratings_id})
                db.execute("DELETE FROM shows WHERE id = :id", {"id": ratings_id})	
                
                # Save (and commit) changes
                db.commit()

exit(0)