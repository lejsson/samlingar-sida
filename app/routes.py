from flask import render_template, request, url_for, redirect, flash, send_from_directory
from flask_sqlalchemy import extension
from flask_wtf.file import FileField
from sqlalchemy import Boolean
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm, NewPostContentForm, EditPostForm, EditPostContentForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post, PostContent 
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from PIL import Image
import os.path, os
import shutil #rm non-empty dirs

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = current_user.posts.all()
    if len(posts) == 0: #Om ej har några samlingar
        zero_posts = True
        return render_template('index.html', title='Your collections', zero_posts=zero_posts)
    postcontents = current_user.postcontents.all()
    user_data_dir = "/static/user_data/" + current_user.username
    return render_template('index.html', title='Your collections', posts=posts, postcontents=postcontents, file_dir=user_data_dir)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/post_content', methods=['GET', 'POST'])
@login_required
def post_content():
    current_post_id = int(request.args.get("current_post_id"))
    current_post = Post.query.get(current_post_id)
    postcontents = current_user.postcontents.all()
    user_data_dir = "/static/user_data/" + current_user.username
    return render_template('post_content.html', postcontents=postcontents, current_post=current_post, file_dir=user_data_dir, title=current_post.title)

@app.route('/singlepost', methods=['GET', 'POST'])
@login_required
def singlepost():
    current_postcontent_id = int(request.args.get("current_postcontent_id"))
    current_postcontent = PostContent.query.get(current_postcontent_id)
    current_post_id = int(request.args.get("current_post_id"))
    current_post = Post.query.get(current_post_id)
    postcontents = current_user.postcontents.all()

    user_data_dir = "/static/user_data/" + current_user.username
    timestamp = current_postcontent.timestamp.date()

    return render_template('singlepost.html', current_post=current_post, postcontents=postcontents, current_postcontent=current_postcontent, file_dir=user_data_dir, timestamp=timestamp, title=current_postcontent.title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'avif', 'webp', 'svg', 'tiff', 'tif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
    form = NewPostForm()
    if form.validate_on_submit():
        image = form.image.data
        extension = os.path.splitext(image.filename)[1]

        collection_dir = os.path.join(app.root_path, 'static') +  '/user_data/' + current_user.username + '/' + form.title.data
        if allowed_file(image.filename):
            if not os.path.exists(collection_dir):
                os.makedirs(collection_dir) #Om inte användarens data dir finns eller om inte diren till collection titeln finns
            else:
                flash("A collection with that title already exists. Please choose a different title.")
                return render_template('addpost.html', title='Add new collection', form=form)
            UPLOAD_FOLDER = collection_dir
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
        else: 
            flash("Filetype not allowed")
            return render_template('addpost.html', title='Add new collection', form=form)

        generated_name = os.popen('python3 app/scripts/randomstring.py 30').read()
        _list = list(generated_name)
        generated_name = ""
        for i in range(len(_list) - 1):
            generated_name += _list[i]
        generated_name += extension
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
    current_post = Post.query.get(current_post_id)

    if form.validate_on_submit():
        image = form.image.data
        extension = os.path.splitext(image.filename)[1]

        if allowed_file(image.filename):
            UPLOAD_FOLDER = os.path.join(app.root_path, 'static') +  '/user_data/' + current_user.username + '/' + current_post.title
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
        else: 
            flash("Filetype not allowed")
            return render_template('addpostcontent.html', title='Add new post', form=form)

        generated_name = os.popen('python3 app/scripts/randomstring.py 30').read()
        _list = list(generated_name)
        generated_name = ""
        for i in range(len(_list) - 1):
            generated_name += _list[i]
        generated_name += extension
        generated_name = secure_filename(generated_name)
        os.rename(os.path.join(UPLOAD_FOLDER, image_filename), os.path.join(UPLOAD_FOLDER, generated_name))

        pc = PostContent(title=form.title.data, description=form.description.data, author=current_user, image=generated_name, parent=current_post_id)
        db.session.add(pc)
        db.session.commit()
        return redirect(url_for('post_content', current_post_id=current_post_id))
        # return redirect(url_for('index'))
    return render_template('addpostcontent.html', title='Add to collection', form=form)

@app.route('/removecollection', methods=['GET'])
@login_required
def removecollection():
    #get vars
    current_post_id = int(request.args.get("current_post_id"))
    current_post = Post.query.get(current_post_id)
    current_post_data_dir = "static/user_data/" + current_user.username + '/' + current_post.title

    #rm collection data dir och allt det innehåller
    shutil.rmtree(os.path.join(app.root_path, current_post_data_dir))

    #remove every post in collection
    current_postcontents = PostContent.query.all()
    for item in current_postcontents:
        if item.parent == current_post.id:
            db.session.delete(item)

    #remove collection from database
    db.session.delete(current_post)
    db.session.commit()
    return redirect('index')

@app.route('/removepostcontent', methods=['GET'])
@login_required
def removepostcontent():
    #get vars
    current_postcontent_id = int(request.args.get("current_postcontent_id"))
    current_postcontent = PostContent.query.get(current_postcontent_id)
    current_post_id = int(request.args.get("current_post_id"))
    current_post = Post.query.get(current_post_id)

    #delete image related to post
    current_postcontent_image_path = "static/user_data/" + current_user.username + '/' + current_post.title + '/' + current_postcontent.image
    #shutil.rmtree(os.path.join(app.root_path, current_postcontent_image_path))
    os.remove(os.path.join(app.root_path, current_postcontent_image_path))

    #remove post
    db.session.delete(current_postcontent)
    db.session.commit()
    return redirect(url_for('post_content', current_post_id=current_post_id))

@app.route('/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    form = EditPostForm()
    current_post_id = int(request.args.get("current_post_id"))
    current_post = Post.query.get(current_post_id)

    if form.validate_on_submit():
        image = form.new_image.data
        extension = os.path.splitext(image.filename)[1]

        collection_dir = os.path.join(app.root_path, 'static') +  '/user_data/' + current_user.username + '/' + form.new_title.data
        if allowed_file(image.filename):
            if not os.path.exists(collection_dir):
                os.makedirs(collection_dir) #Om inte användarens data dir finns eller om inte diren till collection titeln finns
            elif form.new_title.data == current_post.title:
                pass
            else:
                flash("A collection with that title already exists. Please choose a different title.")
                return render_template('editpost.html', title='Edit collection', form=form)
            UPLOAD_FOLDER = collection_dir
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
        else: 
            flash("Filetype not allowed.")
            return render_template('editpost.html', title='Edit collection', form=form)

        generated_name = os.popen('python3 app/scripts/randomstring.py 30').read()
        _list = list(generated_name)
        generated_name = ""
        for i in range(len(_list) - 1):
            generated_name += _list[i]
        generated_name += extension
        generated_name = secure_filename(generated_name)
        os.rename(os.path.join(UPLOAD_FOLDER, image_filename), os.path.join(UPLOAD_FOLDER, generated_name))

        if form.new_title.data == current_post.title:
            os.remove(os.path.join(collection_dir, current_post.image))
        else:
            #move contents of old dir
            old_dir = os.path.join(app.root_path, 'static') +  '/user_data/' + current_user.username + '/' + current_post.title
            os.remove(os.path.join(old_dir, current_post.image))
            files = os.listdir(old_dir)
            if len(files) != 0: #if not empty
                for file in files:
                    shutil.move(os.path.join(old_dir, file), collection_dir)
            shutil.rmtree(old_dir)

            current_post.title = form.new_title.data
            current_post.description = form.new_desc.data

        current_post.description = form.new_desc.data
        current_post.image = generated_name
        db.session.commit()
        return redirect(url_for('post_content', current_post_id=current_post_id))

    #Pre poulate form
    form.new_title.data = current_post.title
    form.new_desc.data = current_post.description

    return render_template('editpost.html', title='Edit collection', form=form)

@app.route('/editpostcontent', methods=['GET', 'POST'])
@login_required
def editpostcontent():
    form = EditPostContentForm()
    current_post_id = int(request.args.get("current_post_id"))
    current_post = Post.query.get(current_post_id)
    current_postcontent_id = int(request.args.get("current_postcontent_id"))
    current_postcontent = PostContent.query.get(current_postcontent_id)
    collection_dir = os.path.join(app.root_path, 'static') +  '/user_data/' + current_user.username + '/' + current_post.title

    if form.validate_on_submit():
        image = form.new_image.data
        extension = os.path.splitext(image.filename)[1]

        if allowed_file(image.filename):
            UPLOAD_FOLDER = collection_dir
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
        else: 
            flash("Filetype not allowed.")
            return render_template('editpostcontent.html', title='Edit post', form=form)

        generated_name = os.popen('python3 app/scripts/randomstring.py 30').read()
        _list = list(generated_name)
        generated_name = ""
        for i in range(len(_list) - 1):
            generated_name += _list[i]
        generated_name += extension
        generated_name = secure_filename(generated_name)
        os.rename(os.path.join(UPLOAD_FOLDER, image_filename), os.path.join(UPLOAD_FOLDER, generated_name))

        os.remove(os.path.join(collection_dir, current_postcontent.image))
        current_postcontent.title = form.new_title.data
        current_postcontent.description = form.new_desc.data
        current_postcontent.image = generated_name
        db.session.commit()
        return redirect(url_for('singlepost', current_post_id=current_post_id, current_postcontent_id=current_postcontent_id))

    #Pre poulate form
    form.new_title.data = current_postcontent.title
    form.new_desc.data = current_postcontent.description
    form.new_image.data = Image.open(os.path.join(collection_dir, current_postcontent.image))

    return render_template('editpostcontent.html', title='Edit post', form=form)
