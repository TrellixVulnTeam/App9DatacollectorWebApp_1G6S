from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123456@192.168.3.2:5432/height_collector'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://qrfgalrkmmrblp:8df946d1e500bb5e410ff565c32c7984bf012e8b34c7a77fa527eb26f0c3c4fb@ec2-50-19-224-165.compute-1.amazonaws.com:5432/dftul29sg000a?sslmode=require'
db=SQLAlchemy(app)

#create inherted class from Model class of SQLAlchemy
class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_ #intialize global variables
        self.height_=height_ #intialize global variables

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        print(email,height)
        if db.session.query(Data).filter(Data.email_==email).count() == 0: # check if email exists on database and add
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            qresult=db.session.query(Data).filter(Data.email_==email).count()
            return render_template("success.html", qresult=qresult)
        return render_template("index.html", message="Email already exists")  #otherwise give message to user  

if __name__ == '__main__'   :
    app.debug=True
    app.run()