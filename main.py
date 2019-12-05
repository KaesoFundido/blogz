from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import html
import os

app=Flask(__name__)
app.config['DEBUG'] =True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://buils-a-blog:pass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

@app.route('/')
#routes to newpost.html
@app.route('/blog')
#routes to blog.html which displays all blog posts

@app.route('/newpost')

blog_title=
blog_body=

app.run()