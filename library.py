# Script to let us navigate a library database and interact with it.
from contextlib import nullcontext

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

def get_status(selected_book):
    cur.execute("SELECT status FROM book WHERE isbn=%s", (selected_book,))

def get_book_and_author():
    cur.execute("SELECT title, first_name, last_name, isbn, genre, status FROM Book b join Author a on a.AuthorID=b.AuthorID")
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

def get_book_with_title(title):
    cur.execute("SELECT b.title, a.first_Name, a.last_Name, b.ISBN, b.genre, b.status From Book b join Author a on a.AuthorID = b.AuthorID where b.title = %s", [title])
    rows = cur.fetchall()
    return rows

def get_book_with_author(author):
    cur.execute("SELECT b.title, a.first_Name, a.last_Name, b.ISBN, b.genre, b.status From Book b join Author a on a.AuthorID = b.AuthorID where a.last_name = %s", [author])
    rows = cur.fetchall()
    return rows

def get_book_with_isbn(isbn):
    cur.execute("SELECT b.title, a.first_Name, a.last_Name, b.ISBN, b.genre, b.status From Book b join Author a on a.AuthorID = b.AuthorID where b.isbn = %s", [isbn])
    rows = cur.fetchall()
    return rows

def get_user_checkouts(user_id):
    cur.execute("""
            SELECT b.ISBN, b.Title, c.DayOut, c.DayDue, c.DayReturned
            FROM Checkout c
            JOIN Book b ON c.ISBN = b.ISBN
            WHERE c.Lib_ID = %s
            ORDER BY c.DayDue
        """, [user_id])
    rows = cur.fetchall()
    return rows

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
            user_id = app.storage.user.get('username')
            ui.navigate.to('/patron_dashboard', user)id  # go to where the user wanted to go
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
            user_id = user_id = app.storage.user.get('username')
            ui.navigate.to('/staff_dashboard', user_id)  # go to where the user wanted to go
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
def patron_dashboard(user_id):
    user_id = app.storage.user.get('username')

    ui.label("📖 Welcome to Your Library Dashboard")

    # Navigation Links
    with ui.row().classes('gap-4'):
        ui.link("🔍 Book Lookup", '/lookup', user_id)
        ui.link("👤 Account Info", '/account')
        ui.link("⭐ Rate a Book", '/rate')


    # Current Books Checked Out or On Hold
    ui.label("📚 Your Books (Checked Out or On Hold)").classes('text-lg mt-4')

    rows = get_user_checkouts(user_id)

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
def staff_dashboard(user_id):
    user_id = app.storage.user.get('username')
    ui.label("📖 Welcome to Your Library Dashboard")

    # Navigation Links
    with ui.row().classes('gap-4'):
        ui.link("🔍 Book Lookup", '/lookup')
        ui.link("👤 Account Info", '/account')
        ui.link("⭐ Rate a Book", '/rate')

    ui.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNNoYnKJ1nuDOlFNvrEzVbS1f6AndwMK--Yg&s')

@ui.page('/lookup')
def book_lookup():
    selected_book = None
    ui.label("Search for books! 📚 Please fill out one of the fields below.")
    with ui.row():
        title=None
        author=None
        isbn=None
        title = ui.input(label = 'Title: ', placeholder='Type a book title')
        author = ui.input(label='Author last: ', placeholder='Type an author last name')
        isbn = ui.input(label='ISBN: ', placeholder='Type an isbn number')
        #print(title.value)
        #author = ui.input('Book author')
        #isbn = ui.input('ISBN')

        ui.button('Search', on_click=lambda:search())
        ui.button('View All', on_click=lambda: view_all())

        ui.separator()

        #ui.label().bind_text_from(title, 'value')

        search_results = ui.table(columns=[{'name': 'title', 'field': 'title', 'label': "Title"},
                                           {'name': 'first_name', 'field': 'first_name', 'label': "Author First"},
                                           {'name': 'last_name', 'field': 'last_name', 'label': "Author Last"},
                                           {'name': 'isbn', 'field': 'isbn', 'label': "ISBN"},
                                           {'name': 'genre', 'field': 'genre', 'label': "Genre"},
                                           {'name': 'status', 'field': 'status', 'label': "Status"}],
                                  rows=[], selection='single', on_select=lambda e: click_book(e))
        ui.button('Hold or checkout book', on_click=lambda: hold_and_checkout_book(selected_book, user_id))
        ui.link('Additional info', '/info_book/{selected_book}')


        def search():
            #ui.label("Results:")
            if title.value:
                book_rows = get_book_with_title(title.value)

            if author.value:
                book_rows = get_book_with_author(author.value)

            if isbn.value:
                book_rows = get_book_with_isbn(int(isbn.value))

            search_results.clear()
            search_results.add_rows(book_rows)
            search_results.update()


        def view_all():
            search_results.add_rows(get_book_and_author())
            search_results.update()

        def click_book(e):
            nonlocal selected_book
            selected_book = int(e.selection[0]['isbn'])

def hold_and_checkout_book(selected_book, user_id):
    dayOut='2025-05-01'
    dayDue='2025-06-01'
    dayReturned=None
    if get_status(selected_book):
        cur.execute("INSERT INTO Checkout(ISBN,Lib_ID,DayOut,DayDue,DayReturned) VALUES (%s, %s, %s, %s, %s)", [selected_book, user_id, dayOut, dayDue, dayReturned])
        conn.commit()
    if not get_status(selected_book):
        cur.execute("INSERT INTO Hold(isbn,dayheld,dayholdexpire,dayout,Lib_ID) VALUES (%s, %s, %s, %s, %s)",
                    [selected_book, dayOut, dayDue, dayReturned, user_id])
        conn.commit()
    ui.navigate.to('/patron_dashboard')

@ui.page('/info_book/{selected_book}')
def info_book(selected_book):
    rows = cur.execute("SELECT * FROM Author a join Book b on a.AuthorID=b.AuthorID WHERE isbn=%s", [selected_book])
    all_book_info = ui.table(columns=[{'name': 'isbn', 'field': 'isbn', 'label': "ISBN"},
                                       {'name': 'title', 'field': 'title', 'label': "Title"},
                                       {'name': 'genre', 'field': 'genre', 'label': "Genre"},
                                       {'name': 'status', 'field': 'status', 'label': "Status"},
                                       {'name': 'publisher', 'field': 'publisher', 'label': "Publisher"},
                                       {'name': 'pub_date', 'field': 'pub_date', 'label': "Date Published"},
                                       {'name': 'first_name', 'field': 'first_name', 'label': "Author first"},
                                       {'name': 'last_name', 'field': 'last_name', 'label': "Author last"},
                                       {'name': 'isbn', 'field': 'isbn', 'label': "ISBN"},
                                       ], rows=[])
    all_book_info.add_rows(rows)
    all_book_info.update()



ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED', port = 8081)