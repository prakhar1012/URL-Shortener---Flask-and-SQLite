from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app=Flask(__name__)

######### SQL Alchemy configuration...

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app, db)

######### Model Creation....

class URL_History(db.Model):
    __tablename__='URL_Shortener'
    id=db.Column(db.Integer,primary_key=True)
    Original_URL=db.Column(db.Text)
    Shorten_URL = db.Column(db.Text)
    #Here id is considered as a primary key

    def __init__(self,Original_URL,Shorten_URL): 
        self.Original_URL=Original_URL
        self.Shorten_URL=Shorten_URL

    def __repr__(self):
        return "Original URL - {} and Shorten URL - {}".format(self.Original_URL,self.Shorten_URL)
    


####################

import pyshorteners

#pyshorteners is a Python library to short and expand urls

OG_URL=''
Shortn_url=''

@app.route('/',methods=["GET","POST"])
def home():

    global OG_URL
    global Shortn_url
    
    if request.method=='POST':
        OG_URL=request.form.get('in_1')
        t= pyshorteners.Shortener()
        Shortn_url = t.tinyurl.short(OG_URL)
        url_append=URL_History(OG_URL,Shortn_url)
        db.session.add(url_append)
        db.session.commit()

    return render_template('home.html',s=Shortn_url)


@app.route('/History',methods=['GET','POST'])
def history():
    
    detail= URL_History.query.all()
    return render_template('history.html', content=detail)
    


if __name__=="__main__":
    app.run(debug=True)


