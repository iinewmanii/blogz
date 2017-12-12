import cgi
from flask import Flask, redirect, request, session, flash, render_template, url_for, escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Newman13@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

website = "Build A Blog"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20))
#     password = db.Column(db.String(20))

#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def __repr__(self):
#         return '<User %r>' % self.username

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

posts = db.session.query(Blog).count()
title = db.session.query(Blog.title).all()
body = db.session.query(Blog.body).all()

def get_blog_list():
    return db.session.query(Blog).all()

@app.route("/blog", methods=['POST', 'GET'])
def blog_page():
    if request.method == 'GET':
        id = request.args.get('id')
        blog = db.session.query(Blog).filter_by(id=id).first()
        return render_template('blogpage.html', title=blog.title, body=blog.body)

    else:
        return render_template('blogpage.html')

@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']

        if (not blog_title) or (blog_title.strip() == ""):
            if blog_body is not None:
                session['body'] = blog_body
                print(session['body'])
            flash("Please give your blog post a title.")
            return render_template("newpost.html", body=session['body'])

        if (not blog_body) or (blog_body.strip() == ""):
            if blog_title is not None:
                session['title'] = blog_title
                print(session['title'])
            flash("Your blog post is empty. Please add content.")
            return render_template('newpost.html', title=session['title'])

        post = Blog(blog_title, blog_body)
        db.session.add(post)
        db.session.commit()
        url = '/blog?id=' + str(post.id)
        return redirect(url)
    
    else:
        return render_template('newpost.html')

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('blog.html', website=website,
                           title=title, body=body, posts=posts, blog=get_blog_list())

app.secret_key = "secret"

if __name__=="__main__":
    app.run()
