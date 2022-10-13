#importing
import sys
import mysql.connector
from mysql.connector import errorcode

#configuration object
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

def viewMenu():
    print('\n -- Main Menu -- \n')
    print(' 1: View our books\n 2: View our store locations\n 3: View your account\n 4: Exit the program')
    try:
        choiceInput = int(input('Please select an option. '))
        return choiceInput

    except ValueError:
        print('\nInvalid input, please try again.')
        sys.exit(0)           

def viewBooks(_cursor):
    _cursor.execute('SELECT book_id, book_name, author, details FROM book')
    books = _cursor.fetchall()

    print('\n-- Displaying our books --')

    for book in books:
        print('\nBook Name: {}'.format(book[1]),
              '\nBook ID: {}'.format(book[0]),
              '\nAuthor Name: {}'.format(book[2]),
              '\nBook Details: {}'.format(book[3]))

def viewLocations(_cursor):
    _cursor.execute("SELECT store_id, locale FROM store")
    storeLocations = _cursor.fetchall()

    print('\n-- Our store locations --')

    for store in storeLocations:
        print('\nStore Location: {}'.format(store[1]),
              '\nStore ID: {}'.format(store[0]))

def authorizeUser():
    try:
        user_id = int(input('\nPlease enter your customer ID (currently 1, 2, or 3): '))
        if user_id < 0 or user_id > 3:
            print("\nInvalid customer number\n")
            sys.exit(0)
            
        return user_id
    except ValueError:
        print('\nInvalid number')
        sys.exit(0)

    

def viewAccountMenu():
    print('\n-- Account Menu --')
    print('\n 1: Your wishlist\n 2: Add to your wishlist\n 3: Back to main menu')
    try:
        accountChoiceInput = int(input('Please select an option.'))
        return accountChoiceInput
    except ValueError:
        print('\nInvalid input, please try again.')
        sys.exit(0)

def viewWishlist(_cursor, _user_id):
    _cursor.execute('SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author ' +
                    'FROM wishlist ' +
                    'INNER JOIN user ON wishlist.user_id = user.user_id ' +
                    'INNER JOIN book ON wishlist.book_id = book.book_id ' +
                    'WHERE user.user_id = {}'.format(_user_id))
    wishlist = _cursor.fetchall()
    print('-- Items in your wishlist--')

    for book in wishlist:
        print('Book Name: {}\n'.format(book[4]),
              'Author Name: {}\n'.format(book[5]),
              'Book ID: {}\n'.format(book[3]))

def viewBooksToAdd(_cursor, _user_id):
    query = ('SELECT book_id, book_name, author, details '
            'FROM book '
            'WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})'.format(_user_id))
    _cursor.execute(query)
    booksToAdd = _cursor.fetchall()

    print('\n-- Books available to add --')

    for book in booksToAdd:
        print('Book Name: {}\n'.format(book[1]),
              'Book ID: {}\n'.format(book[0]))

def addToWishlist(_cursor, _user_id, _book_id):
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))

try:
    db = mysql.connector.connect(**config) # connect to the WhatABook database 

    cursor = db.cursor() # cursor for MySQL queries

    print("\n  Welcome to the WhatABook Application! ")

    userChoice = viewMenu()

    while userChoice != 4:

        if userChoice == 1:
            viewBooks(cursor)

        if userChoice == 2:
            viewLocations(cursor)

        if userChoice == 3:
            tempUserID = authorizeUser()
            userAccountChoice = viewAccountMenu()

            while userAccountChoice != 3:

                if userAccountChoice == 1:
                    viewWishlist(cursor, tempUserID)

                if userAccountChoice == 2:
                    viewBooksToAdd(cursor, tempUserID)

                    book_id = int(input('Please enter the ID of the book you would like to add'))

                    addToWishlist(cursor, tempUserID, book_id)

                    db.commit()

                    print('\nBook with ID {} has been added to your wishlist.'.format())

                if userAccountChoice < 1 or userAccountChoice > 3:
                    print('Invalid option, please try again. ')

                userAccountChoice = viewAccountMenu()

        if userChoice < 0 or userChoice > 4:
            print('Invalid option, please try again. ') 

        userChoice = viewMenu()

    print('\n\n-- Program ended --')    

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print('Uh oh, there was an error:\n', err)

finally:
    """ close the connection to MySQL """

    db.close()
