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
db.execute("CREATE TABLE shows (id INT PRIMARY KEY, title TEXT, year NUMERIC, genres TEXT, rating REAL, numVotes REAL, ranking REAL)")

# The `genres` table will have a column called `show_id` that references the `shows` table above
db.execute("DROP TABLE if exists genres CASCADE")
db.execute("CREATE TABLE genres (show_id INT, genre TEXT, FOREIGN KEY(show_id) REFERENCES shows(id) ON DELETE CASCADE)")

# Open TSV file
# https://datasets.imdbws.com/title.basics.tsv.gz and https://datasets.imdbws.com/title.ratings.tsv.gz
with open("title.basics.tsv", "r") as titles:

    # Create DictReaders
    reader = csv.DictReader(titles, delimiter="\t")
    # ratings_reader = csv.DictReader(ratings, delimiter="\t")

    # Iterate over TSV file
    for row in reader:

        # If non-adult TV show
        if row["titleType"] == "movie" and row["isAdult"] == "0":

            # If year not missing
            if row["startYear"] != "\\N":

                # If since 1970
                startYear = int(row["startYear"])
                if startYear >= 1970:
                # print(row)

                    # Trim prefix from tconst
                    id = int(row["tconst"][2:])
                
                    # Insert show
                    db.execute("INSERT INTO shows (id, title, year, genres) VALUES(:id, :title, :year, :genres)", {"id": id, "title": row["primaryTitle"], "year": startYear, "genres": row['genres']})

                    # Insert genres
                    if row["genres"] != "\\N":
                    
                        for genre in row["genres"].split(","):
                            db.execute("INSERT INTO genres (show_id, genre) VALUES(:id, :genre)", {"id": id, "genre": genre})

                        # Save (and commit) changes    
                        db.commit()

exit(0)