from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pass@localhost:5432/blood-doners"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# user model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email=db.Column(db.String(128))
    mobile=db.Column(db.String(100))
    blood_group=db.Column(db.Integer)

# post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mobile=db.Column(db.String(100))
    blood_group=db.Column(db.Integer)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())


@app.route('/')
def hello_world():
    # return 'Hello, World!'
    return render_template('index.html')

if __name__ == '__main__':
    app.run()