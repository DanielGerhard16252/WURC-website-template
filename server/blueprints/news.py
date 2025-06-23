from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_schema import db, Admin, NewsPost
from flask_login import login_required, current_user
from server.forms.news_forms import NewsPostForm

news_bp = Blueprint('news', __name__)

@news_bp.route('/', methods=['GET'])
def news():
    """
    GET: Displays the news page with all news posts, sorted by creation date.
    """
    posts = NewsPost.query.order_by(NewsPost.created_at.desc()).all()
    return render_template("news/news.html", posts=posts)

@news_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_news():
    """
    GET: Displays the form to create a new news post.
    POST: Handles the creation of a new news post.
    """
    if not current_user.is_authenticated:
        flash("You do not have permission to create news posts.", "danger")
        return redirect(url_for('news.news'))

    form = NewsPostForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        summary = form.summary.data

        new_post = NewsPost(title=title, summary=summary, content=content, creator_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash("News post created successfully!", "success")
        return redirect(url_for('news.news'))

    return render_template("news/create_news.html", form=form)

@news_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_news(post_id):
    """
    GET: Displays the form to edit an existing news post.
    POST: Handles the update of an existing news post.
    """
    post = NewsPost.query.get_or_404(post_id)

    form = NewsPostForm(obj=post)

    if form.validate_on_submit():
        post.summary = form.summary.data
        post.content = form.content.data
        db.session.commit()

        flash("News post updated successfully!", "success")
        return redirect(url_for('news.news'))

    return render_template("news/edit_news.html", form=form, post=post)

@news_bp.route('/delete/<int:post_id>')
@login_required
def delete_news(post_id):
    """
    GET: Deletes a news post. (Yes, this is a GET for simplicity, but should be a DELETE)
    """
    post = NewsPost.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash("News post deleted successfully!", "success")
    return redirect(url_for('news.news'))

@news_bp.route('/<int:post_id>', methods=['GET'])
def view_news(post_id):
    """
    GET: Displays a single news post.
    """
    post = NewsPost.query.get_or_404(post_id)
    return render_template("news/view_news.html", post=post)


