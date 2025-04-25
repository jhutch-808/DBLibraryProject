# Script to let us fill our tables with data.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

def main():
    # Connect to an existing database
    conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

    # Open a cursor to perform database operations
    cur = conn.cursor(row_factory=dict_row)

    #cur.execute("DELETE FROM Author")
    #cur.execute("DELETE FROM Books")
    #cur.execute("DELETE FROM Checkout")
    #cur.execute("DELETE FROM Creditcards")
    #cur.execute("DELETE FROM Patron")
    #cur.execute("DELETE FROM Ratings")
    #cur.execute("DELETE FROM Staff")

    #with open("Author.csv", 'r') as file:
    #     with cur.copy(f"COPY Author FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
    #        copy.write(file.read())
    #conn.commit()
#
    #with open("Books.csv", 'r') as file:
    #    with cur.copy(f"COPY Book FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
    #        copy.write(file.read())
    #conn.commit()
#
    #with open("Checkout.csv", 'r') as file:
    #    with cur.copy(f"COPY Checkout FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
    #        copy.write(file.read())
    #conn.commit()
#
    #with open("Users.csv", 'r') as file:
    #    with cur.copy(f"COPY Users FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
    #        copy.write(file.read())
    #conn.commit()
#
    #with open("Patron.csv", 'r') as file:
    #    with cur.copy(f"COPY Patron FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
    #        copy.write(file.read())
    #conn.commit()
#
    #with open("Creditcards.csv", 'r') as file:
    #    with cur.copy(f"COPY Creditcard FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
    #        copy.write(file.read())
    #conn.commit()


#    with open("Ratings.csv", 'r') as file:
#        with cur.copy(f"COPY Rating FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
#            copy.write(file.read())
#    conn.commit()
#
    with open("Staff.csv", 'r') as file:
        with cur.copy(f"COPY Staff FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

main()