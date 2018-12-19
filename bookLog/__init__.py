from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('application.config')

# db = SQLAlchemy(app)

import application.views
