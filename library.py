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

global user_id

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

def get_creditcards(lib_id):
    cur.execute(f"SELECT Credit_card_num FROM Creditcard WHERE lib_id ={lib_id}")
    rows = cur.fetchall()
    return rows

def get_patron(lib_id):
    cur.execute(f"SELECT * FROM Patron WHERE lib_id ={lib_id}")
    row = cur.fetchall()
    return row

def get_name(lib_id):
    cur.execute(f"SELECT first_name FROM patron inner join users on patron.lib_id = users.lib_id WHERE patron.lib_id = {lib_id}")
    row = cur.fetchall()
    return row

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

def get_all_books():
    cur.execute("SELECT isbn, title, A.first_name, genre FROM Book B join Author A ON B.authorid = A.authorid")
    return cur.fetchall()

def add_rating(isbn, rating, review, lib_id):
    cur.execute("INSERT INTO Rating (isbn, lib_id, rating, review_text) VALUES (%s, %s, %s, %s);",
        (isbn, lib_id, rating, review))
    conn.commit()


def get_rated_books(lib_id):
    cur.execute(f"SELECT B.title, R.rating, R.review_text FROM Rating R JOIN Book B on R.isbn = B.isbn WHERE R.lib_id = {lib_id} ORDER BY R.rating DESC")
    return cur.fetchall()

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
def staff_dashboard():

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


        def search():
            ui.label("Results:")
            if title.value:
                book_rows = get_book_with_title(title.value)

            if author.value:
                book_rows = get_book_with_author(author.value)

            if isbn.value:
                book_rows = get_book_with_isbn(int(isbn.value))

            search_results.add_rows(book_rows)
            search_results.update()


        def view_all():
            search_results.add_rows(get_book_and_author())
            search_results.update()

        def click_book(e):
            nonlocal selected_book
            selected_book = int(e.selection[0]['isbn'])

def hold_and_checkout_book(selected_book):
    dayOut='2025-05-01'
    dayDue='2025-06-01'
    dayReturned=None
    if get_status(selected_book):
        cur.execute("INSERT INTO Checkout(ISBN,Lib_ID,DayOut,DayDue,DayReturned) VALUES (%d, %d, %s, %s, %s)", [selected_book, user_id, dayOut, dayDue, dayReturned])
        conn.commit()
    if not get_status(selected_book):
        cur.execute("INSERT INTO Hold(isbn,dayheld,dayholdexpire,dayout,Lib_ID) VALUES (%d, %d, %s, %s, %s)",
                    [selected_book, dayOut, dayDue, dayReturned, user_id])
        conn.commit()
    patron_dashboard()

def info_book(selected_book):
    rows = cur.execute("SELECT * FROM Author a join Book b on a.AuthorID=b.AuthourID")
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

#NOTE: rows return rows of dictionaries aka rows of maps in java terms
@ui.page('/account')
def account_info():
    user_id = app.storage.user.get('username')
    name = get_name(user_id)
    ui.label(f"🐱🐱🐱🐱🐱🐱🐱 Hello {name[0]['first_name']}! 🐱🐱🐱🐱🐱🐱🐱")
    patron_info = get_patron(user_id)
    creditCard_info = get_creditcards(user_id)
    with ui.card():
        ui.label(f"Library ID: {user_id}")
        ui.label(f" Genre: {patron_info[0]['favgenre']}")
        ui.label(f" address: {patron_info[0]['address']} , { patron_info[0]['city']}, {patron_info[0]['state']}")
        ui.label(f" Credit Card: {creditCard_info[0]['credit_card_num']}")
        ui.button('Back', on_click= lambda: ui.navigate.to('/patron_dashboard'))

@ui.page('/rate')
def rate_page():
    user_id = app.storage.user.get('username')

    def open_rating_dialog(isbn, title):
        with ui.dialog() as dialog, ui.card():
            ui.label(f'Rate "{title}"').classes('text-lg')
            rating_slider = ui.slider(min=1, max=5, value=3, step=1).classes('w-full')
            review_input = ui.textarea(label='Write a short review (optional)', placeholder='Your thoughts...')
            ui.button('Submit', on_click=lambda: submit_rating(isbn, rating_slider.value, review_input.value, dialog))
        dialog.open()

    def submit_rating(isbn, rating, review, dialog):
        add_rating(isbn, rating, review, user_id)
        dialog.close()
        ui.notify('Rating submitted!', type='positive')
        update_rating_panel()
    
    with ui.row().classes('w-full'):

        with ui.column().classes('w-2/3'):
            ui.label('Select a Book to Rate').classes('text-xl')

            for  book in get_all_books():  # Assuming get_all_books() now returns title, author, and genre
                isbn = book['isbn']
                title = book['title']
                author = book['first_name']
                genre = book['genre']
            
                with ui.row().classes('py-2'):
                    ui.label(f'{title} by {author}').classes('text-lg')
                    ui.label(f'Genre: {genre}').classes('text-sm text-gray-500')
                    ui.button('Rate', on_click=lambda isbn=isbn, title=title: open_rating_dialog(isbn, title))

        with ui.column().classes('w-1/3 border-l pl-4'):
            rating_panel = ui.column().classes('w-full')
            ui.label('Your Rated Books (High → Low)').classes('text-lg')

            def update_rating_panel():
                rating_panel.clear()
                for rate in get_rated_books(user_id):
                    title = rate['title']
                    rating = rate['rating']
                    review = rate['review_text']
                    with rating_panel:
                        ui.label(f'⭐ {rating}/5 - {title}')
                        if review:
                            ui.label(f'"{review}"').classes('text-sm text-gray-500')

            update_rating_panel()
    
    ui.button('Back', on_click=lambda: ui.navigate.to('/patron_dashboard'))


ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED', port = 8081)






