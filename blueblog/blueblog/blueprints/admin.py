from flask import Blueprint, request, current_app, render_template, flash, \
                    redirect, url_for
from flask_login import login_required
from blueblog.models import Post, Category
from blueblog.forms import PostForm
from blueblog.extensions import db
from blueblog.utils import redirect_back


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUEBLOG_POST_PER_PAGE']
    )
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination,
                           posts=posts)

@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)

@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)

@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect_back()

@admin_bp.route('/post/category', methods=['GET', 'POST'])
@login_required
def new_category():
    pass

@admin_bp.route('/post/2')
@login_required
def manage_category():
    pass

@admin_bp.route('/post/3')
@login_required
def manage_comment():
    pass

@admin_bp.route('/post/4')
@login_required
def settings():
    pass