from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
import html
import os

app=Flask(__name__)
app.config['DEBUG'] =True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogz:pass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db= SQLAlchemy(app)
app.secret_key='jdfhkaskdjfha;d'

class blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(500))
    blogger= db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, entry, blogger):
        self.title = title
        self.entry = entry
        self.blogger = blogger

class user(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(120))
    password=db.Column(db.String(120))
    blogs= db.relationship('blogpost', backref='user')

    def __init__(self,username, password):
        self.username = username
        self.password=password

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', allusers=user.query.all())

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if username=='' or password=='' or verify=='':
            return render_template('signup.html', error= "One or more fields invalid.")

        existing_user = user.query.filter_by(username=username).first()
        if existing_user != None:
            return render_template('signup.html', error="Username already exists.")
            
        if verify != password:
            return render_template('signup.html', error="Password and Validation do not match.")  

        if len(password) < 3 or len(password) > 20 or ' ' in password:
            return render_template('signup.html', error = "Invalid password")

        if len(username) < 3 or len(username) > 20 or ' ' in username:
            return render_template('signup.html', error = "Invalid username")

        new_user = user(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/newpost')

    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
        password = request.form['password']
        username = request.form['username']

        ispost = request.method

        existing_user = user.query.filter_by(username=username).first()
        if existing_user != None:
            if password == existing_user.password:
                session['username'] = username
                return redirect('/newpost')

            else:
                return render_template('login.html', error="Password is incorrect.")

        else:
            return render_template('login.html', error="Username does not exist.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def blog():
    id=request.args.get('id', default=-1)
    userid=request.args.get('user', default=None)
    if id == -1:
        if userid == None:
            return render_template('blog.html', users = user.query.all())
        else:
            return render_template('SingleUser.html', user = user.query.filter_by(username=userid).first())
    else:
        singleblog = blogpost.query.get(id)
        singleuser = user.query.get(singleblog.blogger)
        return render_template('blog.html', singleblog = singleblog, user = singleuser)



@app.route('/newpost', methods=['GET','POST'])
def newpost():
    
    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']

        if title == '' or entry == '':
            return render_template('newpost.html', title=title, entry=entry)
        else:
            blogger= user.query.filter_by(username=session['username']).first()
            blog_post= blogpost(title,entry, blogger.id)
            db.session.add(blog_post)
            db.session.commit()
            return redirect(url_for('blog', id= blog_post.id))
    return render_template('newpost.html', title = '', entry='')


if __name__ == '__main__':
    app.run()