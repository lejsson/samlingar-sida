from flask import render_template, request, url_for, redirect, flash, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post, PostContent 
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os.path

#För att får items i post använd den och sen counta hur många de innehålla

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
@login_required
def index():
    #hej = current_user.posts.all()
    #test = PostContent.query.get(current_user.id)
    # return render_template('index.html', title='Home', user=data.user, posts=data.posts)
    # hejsan = current_user.postcontents.all()
    # items = 0

    # for item in current_user.postcontents.all()
        # if item.parent == post.id:
            # items += 1

    # current_user.posts.all()[]
    posts = current_user.posts.all()
    postcontents = current_user.postcontents.all()
    user_data_dir = "/static/user_data/" + current_user.username
    return render_template('index.html', title='Home', posts=posts, postcontents=postcontents, file_dir=user_data_dir)

# @app.route('/collections')
# def collections():
    # return render_template('collections.html', title='Collections', user=data.user, posts=data.posts)

# @app.route('/post_content')
# def post_content():
    # return render_template('post-content.html', title=parent, user=data.user, posts=data.posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        # if user is None or not user.check_password(form.password.data):
            # flash('Invalid username or password')
            # return redirect(url_for('login'))
        # login_user(user, remember=form.remember_me.data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page) # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign up', form=form)

UPLOAD_FOLDER = '/static/user_data/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    # pass
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title, description=form.description, author=current_user)
        db.session.add(post)
        db.session.commit()
        image = form.image
        return redirect('index')
    return render_template('addpost.html', title='Add new post', form=form)
