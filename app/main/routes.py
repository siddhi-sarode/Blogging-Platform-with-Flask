from app.forms import PostForm, CommentForm

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

# --- NEW: Search Route ---
@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    # Search by title or content containing the query string
    filters = (Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))
    pagination = Post.query.filter(filters).order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    
    return render_template('search_results.html', posts=pagination.items, pagination=pagination, query=query)
# --- NEW: Tag Filtering Route ---
@bp.route('/tag/<string:tag_name>')
def posts_by_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    # Fetch posts associated with this tag using SQLAlchemy relationship
    pagination = tag.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    
    return render_template('tag_posts.html', tag=tag, posts=pagination.items, pagination=pagination)