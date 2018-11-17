import os
# SQLALCHEMY_DATABASE_URI = 'sqlite:///bookLog.db'
SECRET_KEY = 'secret key'

# firebaseのconfig
FIREBASE_CONFIG = {
    "apiKey": os.environ['FIREBASE_API_KEY'],
    "authDomain": os.environ['FIREBASE_AUTH_DOMAIN'],
    "databaseURL": os.environ['FIREBASE_DATABASE_URL'],
    "storageBucket": os.environ['STORAGE_BUCKET'],
}


#Google Books APIに使うurl
google_books_api_url = 'https://www.googleapis.com/books/v1/volumes?q=id:'