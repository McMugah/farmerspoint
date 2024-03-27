from . import api
from flask import render_template, render_template, redirect, url_for, flash, request,session,jsonify
from flask_login import login_user, current_user, logout_user, login_required
from ..models import User
from urllib.parse import urlparse
from ..forms.user_form import RegistrationForm,LoginForm
from .. import db


@api.route('/')
def get_home():
    return render_template('home.html')


@api.route('/dashboard')
@login_required
def get_dashboard():
    return render_template('dashboard.html')


@api.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    contact_number=form.contact_number.data,
                    address=form.address.data,
                    user_type=form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_token()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('api.login', token=token))  # Redirect to the login page with the token
    return render_template('register.html',  form=form)


@api.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            session['authenticated'] = True  # Set session variable to indicate user is authenticated
            next_page = session.get('next', None)
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('api.get_dashboard'))  # Redirect to homepage if no next page
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)



@api.route('/logout')
def logout():
    logout_user()
    session.pop('authenticated', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('api.get_home'))


@api.route('/profile')
@login_required
def profile():
    user = current_user  # Assuming current_user represents the currently logged-in user
    return render_template('profile.html', user=user)

# @api.route('/profile')
# @login_required
# def profile():
#     user = current_user
#     # Assuming you have a profile_pic attribute in your User model
#     profile_pic_url = user.profile_pic if user.profile_pic else '/static/placeholder.svg'
#     return render_template('profile.html', user=user, profile_pic_url=profile_pic_url)



# Route to render user list
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)

