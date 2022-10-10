# import statements
import sys
import mysql.connector
from mysql.connector import errorcode
# database config object
config = {
 "user": "whatabook_user",
 "password": "MySQL8IsGreat!",
 "host": "127.0.0.1",
 "database": "whatabook",
 "raise_on_warnings": True
}
# create methods!
def show_menu():
 print(" -- Main Menu --")
 print(" 1. View Our Locations \n 2. View Books In Stock \n 3. User Account \n 
4. Exit")
 
 # user input for navigating the site
 try:
 choice = int(input('Enter an option:'))
 return choice
 # for values not listed
 except ValueError:
 print("That was not an option... :(")
 sys.exit(0)
def show_locations(_cursor):
 # query DB for stores
 _cursor.execute("SELECT store_id, locale FROM store")
 
 #get results
 locations = _cursor.fetchall()
 
 # display results
 print("--Stores--")
 
 for location in locations:
 print("Locale: {}\n".format(location[1]))
 
def show_books(_cursor):
 # query DB for books
 _cursor.execute ("SELECT book_id, book_name, author, details FROM book")
 
 # get results
 books = _cursor.fetchall()
 
 # display results
 print("-- Books! --")
 for book in books:
 print("Book ID: {}\n Book Name:{}\n Author: {}\n Details: 
{}\n".format(book[0], book[1], book[2], book[3]))
def validate_user():
 #input user ID
 try:
 user_id = int(input('Enter user ID:'))
 
 #validate choice
 if user_id < 0 or user_id > 3:
 print(" Invalid option")
 sys.exit(0)
 return user_id
 
 #terminate program upon error
 except ValueError:
 print(" Invalid option")
 sys.exit(0)
 
def show_account_menu():
 # Display User Menu
 try:
 print("-- Customer Menu --")
 print("1. View Wishlist \n 2. Add Book to Wishlist \n 3. Return to the Main
Menu")
 account_option = int(input('Choose an option!'))
 return account_option
 
 # Close the program if the account_option is invalid
 except ValueError:
 print("Invalid option")
 sys.exit(0)
def show_wishlist(_cursor, _user_id):
 # Query for a list of the books available
 _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, 
book.book_id, book.book_name, book.author " + "FROM wishlist " + "INNER JOIN user 
ON wishlist.user_id = user.user_id " + "INNER JOIN book ON wishlist.book_id = 
book.book_id " + "WHERE user.user_id = {}".format(_user_id))
 
 # get results
 wishlist = _cursor.fetchall()
 
 # display results
 print("-- Wishlist! --")
 
 for book in wishlist:
 print("Book Name:{}\n Author:{}\n".format(book[4], book[5]))
 
def show_books_to_add(_cursor, _user_id):
 # query for the list of books eligible to be added
 query = ("SELECT book_id, book_name, author, details FROM book WHERE book_id 
NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))
 
 # display
 print(query)
 
 # display results
 _cursor.execute(query)
 books_to_add = _cursor.fetchall()
 
 # print books
 print("-- Available Books --")
 
 for book in books_to_add:
 print("Book ID: {}\n Book Name:{}\n".format(book[0], book[1]))
 
def add_book_to_wishlist(_cursor, _user_id, _book_id):
 _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, 
{})".format(_user_id, _book_id))
 
try:
 # for handling errors w/ connecting to DB
 # connect
 db = mysql.connector.connect(**config)
 
 # for the queries
 cursor = db.cursor()
 
 # print
 print("Welcome!")
 
 # show the main menu
 user_selection = show_menu()
 
 # while the user's selection is not 4 - exit option
 while user_selection != 4:
 # show locations
 if user_selection == 1:
 show_locations(cursor)
 # show books
 if user_selection == 2:
 show_books(cursor)
 # go to user menu
 # validate the ID
 #show account menu
 if user_selection == 3:
 my_user_id = validate_user()
 account_option = show_account_menu()
 # while account option does not equal 3 - exit option
 while account_option != 3:
 # call wishlist
 if account_option == 1:
 show_wishlist(cursor, my_user_id)
 # show books not in the users wishlist
 if account_option == 2:
 # show the books not currently configured in the users wishlist
 show_books_to_add(cursor, my_user_id)
 # get the book_id 
 book_id = int(input(" Enter the id of the book you want to add:"))
# add the selected book the users wishlist
 add_book_to_wishlist(cursor, my_user_id, book_id)
 #commit changes
 db.commit()
 print(" Book ID: {} was added to your 
wishlist!".format(book_id))
 # if the selected option is less than 0 or greater than 3, display 
an invalid user selection 
 if account_option < 0 or account_option > 3:
 print(" That was not a valid ID")
 # show the account menu 
 account_option = show_account_menu()
 
 # display invalid selection
 if user_selection < 0 or user_selection > 4:
 print(" That was not an option")
 
 # show the main menu
 user_selection = show_menu()
 
except mysql.connector.Error as err:
 
 #handle errors
 if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
 print(" One of the supplied credentials are invalid")
 elif err.errno == errorcode.ER_BAD_DB_ERROR:
 print(" Database does not exist")
 else:
 print(err)
finally:
 # close the connection to MySQL
 db.close()
