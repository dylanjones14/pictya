import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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

# Configure SQLite database
# db = SQL("sqlite:///finance.db")
# conn = sqlite3.connect('pictya.db', check_same_thread=False)
# db = conn.cursor()

@app.route("/")
@login_required
def index():
    """Shows main homepage"""

    return render_template("index.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    conn = sqlite3.connect('pictya.db')
    db = conn.cursor()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          (request.form.get("username"),)).fetchone()


        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[2], request.form.get("password")):
             return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]

        render_template("output.html", output="success")

        # Redirect user to home page
        return redirect("/")

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

    conn = sqlite3.connect('pictya.db')
    db = conn.cursor()

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
        elif db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone() != None:
           return apology("username already exists", 403)

        # Ensure password and confirmation password match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Add user to database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)))
        
        # Save (and commit) changes
        conn.commit()

        # Redirect user to home page
        return redirect("/")

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