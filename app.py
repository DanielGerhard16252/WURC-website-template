from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import LoginManager
from flask_ckeditor import CKEditor, upload_success, upload_fail
from db_schema import db, dbinit
from server.blueprints.auth import auth_bp
from server.blueprints.news import news_bp
from server.blueprints.shop import shop_bp
from server.blueprints.gallery import gallery_bp
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
from server.forms.contact_forms import ContactForm

from dotenv import load_dotenv
from pathlib import Path
from db_schema import Image

# Force load .env file from the correct path
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# App config
app = Flask(__name__)
app.config.update({
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': os.environ.get('SECURITY_KEY', 'default_security_key'),
    'SECURITY_PASSWORD_SALT': os.environ.get('SECURITY_SALT', 'default_security_salt'),
    'CKEDITOR_SERVE_LOCAL': True,
    'CKEDITOR_HEIGHT': 500,
    'UPLOAD_FOLDER': 'uploads',
    'CKEDITOR_FILE_UPLOADER': 'upload',
    'UPLOADED_PATH': 'uploads',
})
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialise extensions
db.init_app(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(shop_bp, url_prefix='/shop')
app.register_blueprint(gallery_bp, url_prefix='/gallery')



# Reset DB (development only)
reset_db = False
if reset_db:
    with app.app_context():
        db.drop_all()
        db.create_all()
        dbinit()

# User loader
@login_manager.user_loader
def load_user(user_id):
    from db_schema import Admin
    return Admin.query.get(int(user_id))

# Template filters
@app.template_filter()
def format_datetime(date: datetime) -> str:
    return date.strftime("%B %d, %Y, %H:%M")

@app.template_filter()
def format_price(price: float) -> str:
    return f"£{price:.2f}"

@app.template_filter("nl2br")
def nl2br(s):
    return s.replace("\n", "<br>\n")

# Routes
@app.route('/')
def home():
    photos = Image.query.filter(
        Image.news_post_id.is_(None),
        Image.shop_item_id.is_(None)
    ).all()
    return render_template('index.html', photos=photos)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/files/<filename>')
def uploaded_files(filename):
    return send_from_directory(app.config['UPLOADED_PATH'], filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print("GMAIL_USER:", os.environ.get("GMAIL_USER"))
    print("GMAIL_PASS:", os.environ.get("GMAIL_PASS"))
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        sender_email = form.email.data
        message = form.message.data

        email = EmailMessage()
        email['Subject'] = f"Message from {name}"
        email['From'] = os.environ.get("GMAIL_USER")
        email['To'] = "warwickrifleclub@gmail.com"
        email.set_content(f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}")

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(os.environ.get("GMAIL_USER"), os.environ.get("GMAIL_PASS"))
                smtp.send_message(email)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending message: {e}", "error")

        return redirect('/contact')

    return render_template("contact.html", form=form)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
