import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    rows = db.execute("SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id =? ORDER BY symbol", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    return render_template("index.html", rows = rows, cash = usd(cash))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # ensure request method is POST
    if request.method == "POST":

        # lookup a stock’s current price using
        # function "lookup" implemented in helpers.py
        stock = lookup(request.form.get("symbol"))
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # ensure stock symbol was submitted
        if not symbol:
            return apology("missing symbol")

        # ensure that stock is valid
        if lookup(symbol.upper()) == None:
            return apology("invalid symbol")

        # ensure amount of shares was submitted
        if not shares:
            return apology("missing shares")

        # ensure inputed number of shares is not an alphabetical string
        if not str.isdigit(shares):
            return apology("invalid shares")

         # ensure number of shares is a positive integer
        if int(shares) <= 0:
            return apology("invalid shares")

        transaction_value = float(shares) * stock["price"]

        user_id =  session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transaction_value:
            return apology("Brokie, you cant afford this!")

        else:
            # update cash in users table for the user
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = user_cash - transaction_value, id = user_id )

            date = datetime.datetime.now()

            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)", user_id, stock["symbol"], shares, stock["price"], date)

            flash("Congratulations! Transaction is successful!")

            return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # select values from db about user's transactions
    rows = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id = session["user_id"])

    for row in rows:
        row["price"] = usd(row["price"])
    return render_template("history.html", rows = rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must give username yo!", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must give password yo", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # renders template for user to look up a stock’s current price
    if request.method == "POST":

        # ensure symbol for quoting stock was submitted
        if not request.form.get("symbol"):
            return apology("Wrong symbol Yo!")
        else:
            # lookup a stock’s current price using
            # function "lookup" implemented in helpers.py
            qt = lookup(request.form.get("symbol").upper())

            # ensure that stock is valid
            if qt == None:
                return apology("Invalid Symbol!")

            # return information about a stock’s current price using
            return render_template("quoted.html", name = qt["name"], price = usd(qt["price"]), symbol = qt["symbol"])

    else:
        # redirect user to quote
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""

    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("enter username")
        if not password:
            return apology("enter password")
        if not confirmation:
            return apology("enter confirmation")

        if password != confirmation:
            return apology("pass not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("username already exists")

        session["user_id"] = new_user

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute("SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id = user_id)
        return render_template("sell.html", symbols = [row["symbol"] for row in symbols_user])

    else:
        symbol = request.form.get("symbol")
        stock = lookup(symbol.upper())
        shares = request.form.get("shares")

        # ensure stock symbol was submitted
        if not symbol:
            return apology("missing symbol")

        # ensure that stock is valid
        if stock == None:
            return apology("invalid symbol")

        # ensure inputed number of shares is not an alphabetical string
        if not str.isdigit(shares):
            return apology("invalid shares")

         # ensure number of shares is a positive integer
        if int(shares) <= 0:
            return apology("invalid shares")

        transaction_value = int(shares) * int(stock["price"])

        user_id =  session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id ", id = user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id=:id AND symbol = :symbol ", id = user_id, symbol = symbol)
        user_shares_true = user_shares[0]["shares"]

        if int(shares) > user_shares_true:
            return apology("don't have enough shares to sell")

        uptd_cash = user_cash + transaction_value
        uptd_shares = user_shares_true - int(shares)

        # update cash in users table for the user
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = uptd_cash, id = user_id )

        date = datetime.datetime.now()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)", user_id, stock["symbol"], uptd_shares, stock["price"], date)

        flash("Congratulations! Sold successfully!")

        return redirect("/")

