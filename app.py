from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123456@192.168.3.2/height_collector'
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

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        print(email,height)
        data=Data(email,height)
        db.session.add(data)
        db.session.commit()
        
        return render_template("success.html")


if __name__ == '__main__'   :
    app.debug=True
    app.run()