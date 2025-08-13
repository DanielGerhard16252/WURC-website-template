from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from db_schema import db, Image


gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

@gallery_bp.route('/')
def gallery():
    photos = Image.query.filter(
        (Image.news_post_id == None) & 
        (Image.shop_item_id == None)
    ).all()
    return render_template('gallery.html', photos=photos)

@gallery_bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
    file = request.files['photo']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        new_photo = Image(filename=filename)
        db.session.add(new_photo)
        db.session.commit()
    return redirect(url_for('gallery.gallery'))

@gallery_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    photo = Image.query.get_or_404(id)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('gallery.gallery'))
