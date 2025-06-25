from flask_login import LoginManager
from flask_mail import Mail
import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from db_schema import db, dbinit
from server.blueprints.auth import auth_bp
from server.blueprints.news import news_bp
from server.blueprints.shop import shop_bp
from datetime import datetime
from flask_ckeditor import CKEditor, upload_success, upload_fail

security_key = os.environ.get('SECURITY_KEY', 'default_security_key')
security_salt = os.environ.get('SECURITY_SALT', 'default_security_salt')

CONFIG_DICT = {
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': security_key,
    'SECURITY_PASSWORD_SALT': security_salt,
    'CKEDITOR_SERVE_LOCAL': True,
    'CKEDITOR_HEIGHT': 500,
    'UPLOAD_FOLDER': 'uploads',
    'CKEDITOR_FILE_UPLOADER': 'upload',
    'UPLOADED_PATH': 'uploads',
}

app = Flask(__name__)
app.config.update(CONFIG_DICT)
db.init_app(app)
ckeditor = CKEditor()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated

login_manager.init_app(app)
mail = Mail(app)
mail.init_app(app)
ckeditor.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(shop_bp, url_prefix='/shop')

reset_db = False
if reset_db:
    with app.app_context():
        db.drop_all()  # Drop all tables if reset_db is True
        db.create_all()  # Create all tables
        dbinit()

@login_manager.user_loader
def load_user(user_id):
    """
    Callback to reload the user object from the user ID stored in the session.
    """
    from db_schema import Admin
    return Admin.query.get(int(user_id))

@app.template_filter()
def format_datetime(date: datetime) -> str:
    """
    Formats a datetime object into a readable string - e.g. "January 5, 2023, 13:49"
    """
    return date.strftime("%B %d, %Y, %H:%M")

@app.template_filter()
def format_price(price: float) -> str:
    """
    Formats a price into a string with two decimal places and a £ - e.g. "£12.34"
    """
    return f"£{price:.2f}"

@app.route('/')
def home():
    """
    GET: Displays the home page.
    """
    return render_template("index.html")

@app.route('/about')
def about():
    """
    GET: Displays the about page.
    """
    return render_template("about.html")

@app.route('/contact')
def contact():
    """
    GET: Displays the contact page.
    """
    return render_template("contact.html")

@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)

if __name__ == '__main__':
    app.run(debug=True)