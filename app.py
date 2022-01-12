from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from twilio.rest import Client


accound_sid="AC7a811a08c6ca0e18b0d157e1dfacd33f"
auth_token="8f998f952bab33ca0d4c54703c1bb669"
twilio_number="+15104803663"

client=Client(accound_sid,auth_token)

def sms_to_doners(phn_nbr,message):
        sms=client.messages.create(
        body=message,
        from_=twilio_number,
        to=phn_nbr
        )
        return sms
def sms_to_client(data):
        client.messages.create(
        body=data,
        from_=twilio_number,
        to=phn_nbr
        )


app = Flask(__name__)
app.debug=True


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pass@localhost:5432/blood-doners"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blood-donation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# user model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
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
        bg=request.form['bg']
        
        create_doner=User(name=name,mobile=mobile,blood_group=bg)
        db.session.add(create_doner)
        db.session.commit()
        return redirect('/')

    return render_template('doner.html')


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
        msg=f"{name} need {bg} blood.Please contact:{mobile}"
        doners_phn=db.session.query(User.mobile).filter(User.blood_group==bg).all()
        doners_phn=[i[0] for i in doners_phn]
        print(type(doners_phn))
        for i in doners_phn:
            phn_nbr='+88'+i
            sms=sms_to_doners(phn_nbr,msg)
            print(sms.body)


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