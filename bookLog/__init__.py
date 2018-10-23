from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('bookLog.config')

# db = SQLAlchemy(app)

import bookLog.views
