from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from server.util.inputs import sanitise_string
from db_schema import db, Admin
from server.forms.auth_forms import LoginForm, RegisterForm, EmailForm, ResetPasswordForm
# from server.util.email import send_email
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from server.util.tokens import generate_reset_token, confirm_reset_token
from datetime import datetime, timedelta

# We are using blueprints (such as this auth.py blurptint) to organize our code better, compared
# to having all the routes in the server file (acs.py).

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: displays the login page
    POST: Handles login logic - checks the data from the request, and logs the user in if the data is correct.
          This includes setting session variables, and redirecting to the correct page.
    Used for both regular users and super user.
    """

    if current_user.is_authenticated:
        # if the user is already logged in redirect to the indx
        return redirect(url_for('index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        email = sanitise_string(form.email.data)
        password = form.password.data
        remember = form.remember.data

        # checking username and password
        user: Admin = Admin.query.filter_by(email=email).first()
        if not user:
            form.email.errors.append("Incorrect email or password")
            return render_template("auth/login.html", form=form)

        hashed_password = user.password_hash
        if not check_password_hash(hashed_password, password):
            form.password.errors.append("Incorrect email or password")
            return render_template("auth/login.html", form=form)
        
        logout_user()

        login_user(user, remember=remember == "on")

        return redirect(url_for('home'))
    
    return render_template("auth/login.html", form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    
    if form.validate_on_submit():
        email = sanitise_string(form.email.data)
        password = form.password.data
        first_name = form.first_name.data.strip() # dotn sanitise as that lowers
        last_name = form.last_name.data.strip()

        # if all the checks are passed, create the user and redirect to the login page
        new_user = Admin(email=email, password_hash=generate_password_hash(password), first_name=first_name, last_name=last_name)
        try:
            db.session.add(new_user)
            db.session.commit()
            
        except IntegrityError:
            form.email.errors.append("An account with that email address already exists!")
            return render_template('auth/register.html', form=form)

        login_user(new_user)

        return redirect(url_for('home'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    This function logs the user out, by popping the email from the session.
    It then redirects to the index.
    """
    logout_user()
    return redirect(url_for('home'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    For when a user forgets their password, this function will send a reset link to their email.
    """

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = EmailForm()
    
    if form.validate_on_submit():
        email = sanitise_string(form.email.data)

        user: Admin = Admin.query.filter_by(email=email).first()

        if not user:
            form.email.errors.append("No account with that email exists.")
            return render_template('auth/forgot_password.html', form=form)
        
        # send the email with the reset link
        token = generate_reset_token(email)
        # add the full URL not just the path to url_for with _external=True
        reset_url = url_for('.reset_password', token=token, _external=True)
        html = render_template('auth/forgot_password_email_content.html', reset_url=reset_url)
        subject = "Reset your password"

        # send_email([email], subject, html)

        flash("An email has been sent to reset your password!", "success")
        return redirect(url_for('.login'))

    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>')
def reset_password(token):
    """
    This route controls what happens when the reset password link is clicked from the forgot
    password email.
    """
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for('index'))
    
    # perform checks on the email and token to ensure both are valid
    try:
        email = confirm_reset_token(token)
    except:
        flash("Invalid or expired reset password link.", "error")
    
    user = Admin.query.filter_by(email=email).first()

    form = ResetPasswordForm()
    if not user:
        abort(404, "No user found for the given email address.")

    elif form.validate_on_submit():
        new_password = form.new_password.data
        user.password_hash = generate_password_hash(new_password)
        db.session.add(user)
        db.session.commit()

        flash("Password changed successfully!", "success")
        return redirect(url_for('.login'))

    # need to show the reset password screen.
    return render_template('auth/reset_password.html', form=form)
