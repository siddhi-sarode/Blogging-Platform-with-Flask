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