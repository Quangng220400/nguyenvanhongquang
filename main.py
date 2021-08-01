from flask_paginate import get_page_parameter, Pagination
from flask import Flask, render_template, flash, session, request
from werkzeug.utils import redirect
from forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from flask_msearch import Search

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QuangNvh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

search = Search()
search.init_app(app)

import models


@app.route('/index')
def Welcome():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email=_email).first()
        if user is None:
            flash('Wrong email address or password!')
        else:
            if user.check_password(_password):
                session['user'] = user.user_id
                return redirect('/home')
            else:
                flash('Wrong email address or password!')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Validate on submit")
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data
        if (db.session.query(models.User).filter_by(email=_email).count() == 0):
            user = models.User(first_name=_fname, last_name=_lname, email=_email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('ReSuccess.html', user=user)
        else:
            flash('Email {} is already exsits!'.format(_email))
            return render_template('register.html', form=form)
    print("Not validate on submit")
    return render_template('register.html', form=form)


@app.route('/LogOut')
def LogOut():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect('/login')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = models.Post(title=post_title,
                               content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = models.Post.query.order_by(models.Post.posted_on).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    to_edit = db.session.query(models.Post).filter_by(id=id).first()
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.posted_by = request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit_post.html', post=to_edit)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = models.Post(title=post_title,
                               content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


@app.route('/search')
def search():
    searchword = request.args.get('q')
    posts = models.Post.query.msearch(searchword, fields=['title'])
    return render_template('result.html', posts=posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = db.session.query(models.Post).filter_by(id=id).first()
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/posts')


if __name__ == '__main__':
    app.run(debug=True)
