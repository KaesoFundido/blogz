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
    entry = db.Column(db.String(120))

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry

class user(db.Model):
    userid=
    email=
    password=

    def__init__(self,email, password):
    self.email=email
    self.password=password

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('blog'))


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