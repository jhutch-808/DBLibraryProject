# Script to let us test the functionality of the courses table.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def list_authors():
    cur.execute("SELECT * FROM Author")
    rows = cur.fetchall()
    print("Here are the authors:")
    for author in rows:
        print("ID:", author['AuthorID'], "first name:", author['First_name'], "Last name:", author['last_name'])

def add_authors_from_csv(filename):
    with open(filename, 'r') as file:
        with cur.copy(f"COPY Author FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

def delete_all_authors():
    cur.execute("DELETE FROM Author")  # careful! deletes everything.
    conn.commit()

def main():
    list_authors()
    delete_all_authors()
    add_authors_from_csv("Author.csv")
    list_authors()


main()
cur.close()
conn.close()