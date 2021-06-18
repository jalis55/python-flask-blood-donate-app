from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime



app = Flask(__name__)
app.debug=True


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pass@localhost:5432/blood-doners"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# user model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    email=db.Column(db.String(128))
    mobile=db.Column(db.String(100))
    blood_group=db.Column(db.String(20))

# post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mobile=db.Column(db.String(100))
    blood_group=db.Column(db.String(20))
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())


@app.route('/')
def hello_world():
    # return 'Hello, World!'
    return render_template('index.html')


@app.route('/doners',methods=['POST','GET'])
def doners():
    if request.method == 'POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        bg=request.form['bg']
        
        create_doner=User(name=name,mobile=mobile,email=email,blood_group=bg)
        db.session.add(create_doner)
        db.session.commit()
        return redirect('/')

    return render_template('doners.html')


@app.route('/donation',methods=['POST','GET'])
def donation():
    if request.method == 'POST':
        name=request.form['name']
        mobile=request.form['mobile']
        bg=request.form['bg']

        create_post=Post(name=name,mobile=mobile,blood_group=bg)
        db.session.add(create_post)
        # db.session.flush()
        # post_id=create_post.id
        # print (id)
        db.session.commit()
        # doners=db.session.query(User).filter(User.blood_group==bg).all()
        # sms service implementation 
        return redirect('/')


    return render_template('donation.html')

@app.route('/all-posts')
def all_posts():
    posts=db.session.query(Post).order_by(Post.id.desc()).all()
    return render_template('posts.html',posts=posts)
@app.route('/doner-list/<string:bg>')
def doner_list(bg):

    doners=db.session.query(User).filter(User.blood_group==bg).all()
    return render_template('doner_list.html',doners=doners)




if __name__ == '__main__':
    app.run()