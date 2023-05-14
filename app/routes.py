from flask import render_template, request, url_for, redirect, flash, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm, NewPostContentForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post, PostContent 
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os.path, os

#För att får items i post använd den och sen counta hur många de innehålla

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = current_user.posts.all()
    postcontents = current_user.postcontents.all()
    user_data_dir = "/static/user_data/" + current_user.username
    return render_template('index.html', title='Home', posts=posts, postcontents=postcontents, file_dir=user_data_dir)

# @app.route('/post_content/<current_user>', methods=['GET', 'POST'])
@app.route('/post_content', methods=['GET', 'POST'])
@login_required
# def post_content(current_user):
def post_content():
    current_post_id = int(request.args.get("current_post_id"))
    posts = Post.query.all()
    current_post = posts[current_post_id - 1]
    # current_post = posts[posts.index(current_post)]
    postcontents = current_user.postcontents.all()
    user_data_dir = "/static/user_data/" + current_user.username
    return render_template('post_content.html', postcontents=postcontents, current_post=current_post, file_dir=user_data_dir, title=current_post.title)
    # return render_template('post_content.html', postcontents=postcontents, current_post=current_post)
    # return render_template('post_content.html', title=post.title, postcontents=postcontents) # Hur jag ska skicka title

@app.route('/singlepost', methods=['GET', 'POST'])
@login_required
def singlepost():
    current_postcontent_id = int(request.args.get("current_postcontent_id"))
    current_post_title = request.args.get("current_post_title")

    postcontents = PostContent.query.all()
    current_postcontent = postcontents[current_postcontent_id - 1]
    user_data_dir = "/static/user_data/" + current_user.username
    timestamp = current_postcontent.timestamp.date()

    return render_template('singlepost.html', current_post_title=current_post_title, postcontents=postcontents, current_postcontent=current_postcontent, file_dir=user_data_dir, timestamp=timestamp, title=current_postcontent.title)

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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
    form = NewPostForm()
    if form.validate_on_submit():
        image = form.image.data
        dir = os.path.join(app.root_path, 'static') +  '/user_data/' + current_user.username + '/' + form.title.data

        if allowed_file(image.filename):
            if not os.path.exists(dir):
                os.mkdir(dir)
            UPLOAD_FOLDER = dir
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
        else: 
            flash("Filetype not allowed")
            return render_template('addpost.html', title='Add new post', form=form)

        generated_name = os.popen('python3 app/scripts/randomstring.py 30').read()
        _list = list(generated_name)
        generated_name = ""
        for i in range(len(_list) - 1):
            generated_name = generated_name + _list[i]
        generated_name = secure_filename(generated_name)
        os.rename(os.path.join(UPLOAD_FOLDER, image_filename), os.path.join(UPLOAD_FOLDER, generated_name))

        post = Post(title=form.title.data, description=form.description.data, author=current_user, image=generated_name)
        db.session.add(post)
        db.session.commit()
        return redirect('index')
    return render_template('addpost.html', title='Add new collection', form=form)

@app.route('/addpostcontent', methods=['GET', 'POST'])
@login_required
def addpostcontent():
    form = NewPostContentForm()
    current_post_id = int(request.args.get("current_post_id"))
    current_post = Post.query.all()[current_post_id - 1]

    if form.validate_on_submit():
        image = form.image.data

        if allowed_file(image.filename):
            UPLOAD_FOLDER = os.path.join(app.root_path, 'static') +  '/user_data/' + current_user.username + '/' + current_post.title
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
        else: 
            flash("Filetype not allowed")
            return render_template('addpostcontent.html', title='Add new post', form=form)

        # os.path.exists("'/static/user_data")
        generated_name = os.popen('python3 app/scripts/randomstring.py 30').read()
        _list = list(generated_name)
        generated_name = ""
        for i in range(len(_list) - 1):
            generated_name = generated_name + _list[i]
        generated_name = secure_filename(generated_name)
        os.rename(os.path.join(UPLOAD_FOLDER, image_filename), os.path.join(UPLOAD_FOLDER, generated_name))

        pc = PostContent(title=form.title.data, description=form.description.data, author=current_user, image=generated_name, parent=current_post_id)
        db.session.add(pc)
        db.session.commit()
        return redirect('index')
    return render_template('addpostcontent.html', title='Add to collection', form=form)
