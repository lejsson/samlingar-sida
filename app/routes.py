from flask import render_template, request, url_for, redirect, flash
from app import app, data
from app.forms import LoginForm

@app.route('/')
@app.route('/index/')
def index():
    # return render_template('index.html', title='Home', user=data.user, posts=data.posts)
    return render_template('index.html', title='Home', posts=data.posts)

@app.route('/collections/')
def collections():
    return render_template('collections.html', title='Collections', user=data.user, posts=data.posts)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        # return redirect('/index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
