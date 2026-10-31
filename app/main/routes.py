from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.main import bp
from app.models import User, Post, Tag, Comment
from app.forms import PostForm, CommentForm, SearchForm
from app import db

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template('index.html', posts=pagination.items, pagination=pagination)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template('user.html', user=user, posts=pagination.items, pagination=pagination)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash("Username exists.")
            return redirect(url_for('main.register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!")
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash("Invalid credentials.")
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    posts = current_user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('dashboard.html', posts=posts)

@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        tag_names = [t.strip() for t in form.tags.data.split(',')] if form.tags.data else []
        for name in tag_names:
            if name:
                tag = Tag.query.filter_by(name=name).first()
                if not tag: tag = Tag(name=name)
                post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!")
        return redirect(url_for('main.dashboard'))
    return render_template('post_form.html', form=form, edit_mode=False)

@bp.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = db.session.get(Post, id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to comment.")
            return redirect(url_for('main.login'))
        comment = Comment(body=form.body.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('main.post', id=post.id))
    
    comments = post.comments.order_by(Comment.timestamp.asc()).all()
    return render_template('post_detail.html', post=post, form=form, comments=comments)

@bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = db.session.get(Post, id)
    if post.author != current_user:
        return redirect(url_for('main.dashboard'))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.tags = []
        tag_names = [t.strip() for t in form.tags.data.split(',')] if form.tags.data else []
        for name in tag_names:
            if name:
                tag = Tag.query.filter_by(name=name).first()
                if not tag: tag = Tag(name=name)
                post.tags.append(tag)
        db.session.commit()
        flash("Post updated!")
        return redirect(url_for('main.post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = ", ".join([tag.name for tag in post.tags])
    return render_template('post_form.html', form=form, edit_mode=True)

@bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = db.session.get(Post, id)
    if post and post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.")
    return redirect(url_for('main.dashboard'))

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    filters = (Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))
    pagination = Post.query.filter(filters).order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template('search_results.html', posts=pagination.items, pagination=pagination, query=query)

@bp.route('/tag/<string:tag_name>')
def posts_by_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = tag.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template('tag_posts.html', tag=tag, posts=pagination.items, pagination=pagination)