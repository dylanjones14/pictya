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

# Delete all movies that exist in shows database, but not in ratings database
db.execute("DELETE from shows WHERE rating IS NULL")

# Save (and commit) changes
db.commit()

# Add the IMDB ranking to shows https://help.imdb.com/article/imdb/track-movies-tv/ratings-faq/G67Y87TFYYP6TWAV#included
db.execute("UPDATE shows SET ranking = ((numvotes / (numvotes + 25000)) * rating) + ((25000 / (numvotes + 25000)) * (SELECT AVG(rating) FROM shows))")

# Save (and commit) changes
db.commit()

exit(0)