from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import html
import os

app=Flask(__name__)
app.config['DEBUG'] =True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogz:pass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db= SQLAlchemy(app)

class blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(500))
    blogger= db.Column(db.Integer)

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry

class user(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(120))
    password=db.Column(db.String(120))
    blogs= db.relationship('blogpost', backref='user.id')

    def__init__(self,email, password):
    username = relationship
    self.password=password

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('blog'))

@app.route('/signup')

@app.route('/login')
def login():
    if request.method=="POST":
        password = request.form['password']
        username = request.form['username']
        email = request.form['email']
        verify = request.form['verify']
        ispost = request.method
        if len(password) > 3 and len(password) < 20 and ' ' not in password:
            if len(username) > 3 and len(username) < 20 and ' ' not in username:
                if verify == password and verify != '':
                    if email == '' or email.count('@') == 1 and email.count('.') == 1 and len(email) > 3 and len(email) < 20 and ' ' not in email:  
                        return redirect(url_for('welcome'), code=307)
        return render_template('index.html', username=username,password=password, verify=verify, email=email, ispost=ispost)


@all.route('/index')


@app.route('/blog', methods=['GET'])
def blog():
    id=request.args.get('id', default=-1)
    if id == -1:
        return render_template('blog.html', blogs = blogpost.query.all())
    else:
        return render_template('blog.html', singleblog = blogpost.query.get(id))



@app.route('/newpost', methods=['GET','POST'])
def newpost():
    
    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
        if title == '' or entry == '':
            return render_template('newpost.html', title=title, entry=entry)
        else:
            blog_post= blogpost(title,entry)
            db.session.add(blog_post)
            db.session.commit()
            return redirect(url_for('blog', id= blog_post.id),code =307)
    return render_template('newpost.html', title = '', entry='')


if __name__ == '__main__':
    app.run()