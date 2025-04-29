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

def get_password_for_user(user_id):
    #print("uid", user_id)
    cur.execute("SELECT First_Name from Users where Lib_Id=%s", [user_id])
    row = cur.fetchone()
    #print("test", row)
    return str(row['first_name'])  # return as a string to simulate a password

def get_password_for_staff(user_id):
    cur.execute("SELECT CellNum from Staff where Lib_Id=%s", [user_id])
    row = cur.fetchone()
    return str(row['cellnum'])  # return as a string to simulate a password


@ui.page('/')
def homepage():
    ui.label("🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱Welcome to the Lynx Library!🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱🐱")
    ui.image('https://d1jyxxz9imt9yb.cloudfront.net/medialib/3891/image/s768x1300/AdobeStock_263655355_433577.jpg')
    ui.link("User Login", '/login')
    ui.link("Staff Login", '/staff_login')
@ui.page('/login')
def login():
    def try_login():

        password = get_password_for_user(username_box.value)
        if password == password_box.value:
            app.storage.user['username'] = username_box.value
            ui.navigate.to('/patron_dashboard')  # go to where the user wanted to go
        else:
            ui.image('https://media.makeameme.org/created/when-your-login.jpg')
            ui.notify('Wrong username or password', color='negative')

    ui.label("Patron Login: Enter your Library ID and First Name")
    with ui.row():
        username_box = ui.input('Library ID')
        password_box = ui.input('First_Name', password=True)
        ui.button('Log in', on_click=try_login)
    ui.image('https://i.imgflip.com/1gtzh0.jpg')



@ui.page('/staff_login')
def staff_login():
    def try_staff_login():
        password = get_password_for_staff(username_box.value)
        if password == password_box.value:
            app.storage.user['username'] = username_box.value
            ui.navigate.to('/staff_dashboard')  # go to where the user wanted to go
        else:
            ui.image('https://media.makeameme.org/created/when-your-login.jpg')
            ui.notify('Wrong username or password', color='negative')


    ui.label("Patron Login: Enter your Library ID and CellNum")
    with ui.row():
        username_box = ui.input('Library ID')
        password_box = ui.input('CellNum', password=True)
        ui.button('Log in', on_click=try_staff_login)
    ui.image('https://i.imgflip.com/1gtzh0.jpg')


@ui.page('/patron_dashboard')
def patron_dashboard():
    user_id = app.storage.user.get('username')

    ui.label("📖 Welcome to Your Library Dashboard")

    # Navigation Links
    with ui.row().classes('gap-4'):
        ui.link("🔍 Book Lookup", '/lookup')
        ui.link("👤 Account Info", '/account')
        ui.link("⭐ Rate a Book", '/rate')


    # Current Books Checked Out or On Hold
    ui.label("📚 Your Books (Checked Out or On Hold)").classes('text-lg mt-4')

    cur.execute("""
        SELECT b.ISBN, b.Title, c.DayOut, c.DayDue, c.DayReturned
        FROM Checkout c
        JOIN Book b ON c.ISBN = b.ISBN
        WHERE c.Lib_ID = %s
        ORDER BY c.DayDue
    """, [user_id])
    rows = cur.fetchall()

    if rows:
        ui.table(columns=[
            {'name': 'ISBN', 'label': 'ISBN', 'field': 'ISBN'},
            {'name': 'Title', 'label': 'Title', 'field': 'Title'},
            {'name': 'DayOut', 'label': 'Checked Out', 'field': 'DayOut'},
            {'name': 'DayDue', 'label': 'Due Date', 'field': 'DayDue'},
            {'name': 'DayReturned', 'label': 'Returned', 'field': 'DayReturned'}
        ], rows=rows)

    ui.image('https://library.missouri.edu/news/wp-content/uploads/sites/53/2020/05/Housewives-300x208.jpg')



@ui.page('/staff_dashboard')
def staff_dashboard():

    ui.label("📖 Welcome to Your Library Dashboard")

    # Navigation Links
    with ui.row().classes('gap-4'):
        ui.link("🔍 Book Lookup", '/lookup')
        ui.link("👤 Account Info", '/account')
        ui.link("⭐ Rate a Book", '/rate')

    ui.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNNoYnKJ1nuDOlFNvrEzVbS1f6AndwMK--Yg&s')




ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED', port = 8081)