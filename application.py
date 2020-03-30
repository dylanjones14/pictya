import os
import cs50
import urllib.parse
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    """Shows main homepage"""

    return render_template("index.html")

@app.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():
    """Shows watchlist"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        f = request.form

        for key in f.keys():
            for value in f.getlist(key):
                return render_template("output.html", output=key, output2=value)

        #for field in request.form:

            #render_template("output.html", output=field.name)

            #print(field.name)
            #print(field.description)
            #print(field.label.text)
            #print(field.data)

            #db.execute("INSERT INTO watchlist(user_id, show_id, watched) VALUES (user=:user_id, show=:show_id, watched=:watched)", {"user_id": session["user_id"], "show_id": XXX, "watched": TRUE/FALSE})

        # SEND FORM DATA TO watchlist table

        return apology("TO DO", 403)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        
        rows = db.execute("SELECT id, title, year, rating, watched FROM shows LEFT JOIN watchlist ON shows.id = watchlist.show_id WHERE rating IS NOT NULL AND rating < 9.4 ORDER BY ranking DESC, title ASC LIMIT 100")
        # rows = db.execute("SELECT id, title, year, rating, watched FROM shows LEFT JOIN watchlist ON shows.id = watchlist.show_id WHERE rating IS NOT NULL AND rating < 9.4 ORDER BY rating DESC, title ASC LIMIT 100")

        return render_template("watchlist.html", rows=rows)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": request.form.get("username")}).fetchone()

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[2], request.form.get("password")):
             return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]

        # Redirect user to home page
        return redirect("/watchlist")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
           return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Check username does not exist
        elif db.execute("SELECT * FROM users WHERE username = :username", {"username": request.form.get("username")}).fetchone():
            return apology("username already exists", 403)

        # Ensure password and confirmation password match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)
        
        # Insert user and password into database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",{"username": request.form.get("username"), "hash": generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)})
        
        # Save (and commit) changes
        db.commit()
        
        # Redirect user to home page
        return redirect("/watchlist")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

        
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
 app.debug = True
 port = int(os.environ.get("PORT", 5000))
 app.run(host='0.0.0.0', port=port)