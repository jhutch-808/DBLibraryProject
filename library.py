# Script to let us navigate a library database and interact with it.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def get_author():
    cur.execute("SELECT First_Name,Last_Name,Publisher,AuthorID FROM Author")
    rows = cur.fetchall()
    return rows

def get_books():
    cur.execute("SELECT ISBN,Title,Genre,AuthorID,Status,Publisher, Pub_date FROM Books")
    rows = cur.fetchall()
    return rows

def get_checkout():
    cur.execute("SELECT ISBN,Lib_ID,DayOut,DayDue,DayReturned FROM Checkout")
    rows = cur.fetchall()
    return rows

def get_creditcards():
    cur.execute("SELECT Lib_ID,Credit_card_num,Exp_date,Pin,Zipcode FROM Creditcards")
    rows = cur.fetchall()
    return rows

def get_patron():
    cur.execute("SELECT Lib_ID,FavGenre,Address FROM Patron")
    rows = cur.fetchall()
    return rows

def get_ratings():
    cur.execute("SELECT ISBN,Lib_ID,Rating,Review_text FROM Ratings")
    rows = cur.fetchall()
    return rows

def get_staff():
    cur.execute("SELECT Lib_ID,Role,CellNum FROM Staff")
    rows = cur.fetchall()
    return rows

def get_users():
    cur.execute("SELECT Lib_ID,First_Name,Last_Name FROM Users")
    rows = cur.fetchall()
    return rows

@ui.page('/')
def homepage():
    ui.label("Welcome to the Lynx Library!")

    username = app.storage.user.get('username', None)  # default if not logged in is None
    if username is not None:
        ui.label("You are logged in as user: " + username)
    else:
        ui.label("You are not logged in.")

    ui.link("Login", '/login')
    ui.link("Logout", '/logout')
    ui.link("Register for classes", '/register')
    ui.link("Drop a class", '/drop')
    ui.link("Password-protected test page", '/protected')
    ui.link("Dashboard", '/dashboard')

