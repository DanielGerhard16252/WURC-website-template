"""
This file contains the database schema for the application - such as news posts, shop items, admin users
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta

# create the database interface
db = SQLAlchemy()

"""
Note that images will be handled by using IDs and storing the images in a folder, so we dont have to store paths.
"""

# Only users we need to track are admins, who can edit the pages (create news pages, shop items etc)
class Admin(UserMixin, db.Model):
    """
    Represents attendees of events - they can buy tickets for different events, and log in.
    The super user can create events and manage them, and there should only be one super user.
    """
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True) # max email length is 254 characters (https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    password_hash = db.Column(db.String(60)) # max password length is 30 characters, password will be hashed.
    # The below are used for email confirmation functionality.
    # email_confirmed = db.Column(db.Boolean, default=False)
    # email_confirmation_last_sent = db.Column(db.DateTime, default=datetime.now())


class NewsPost(db.Model):
    """
    A new post on the site which can be created, edited and deleted by admins.
    """
    __tablename__ = 'news_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(255), nullable=False)  # A short summary of the news post
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    creator_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    # TODO add image support

class ShopItem(db.Model):
    """
    A shop item to display.
    """
    __tablename__ = 'shop_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # URL to the image of the item
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    creator_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    # TODO add image support, or use a file upload system to store images in a folder and link to them here


def dbinit():
    """
    This function is used to initialise the database with the superuser.
    No other sample data is added.
    """
    
    # test data
    db.session.add(Admin(
        email="admin@gmail.com",
        first_name="Admin",
        last_name="User",
        password_hash=generate_password_hash("adminpassword")
    ))
    db.session.add(NewsPost(title="Welcome to the site!", content="This is the first news post on the site. We hope you enjoy your stay!", creator_id=1, created_at=datetime.now(), updated_at=datetime.now(), summary="Welcome to the site!"))
    db.session.add(ShopItem(name="Sample Item", description="This is a sample item for the shop.", price=19.99, image_url="https://example.com/sample-item.jpg", creator_id=1))
    db.session.commit()