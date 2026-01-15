from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from src.models.user_model import User
from src.models.listing_model import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        user = User.query.filter_by(phone_number=phone).first()
        
        # Check if user exists AND password is correct
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('web.dashboard')) # We will create this view next
        else:
            flash('Invalid phone number or password.', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        phone = request.form.get('phone')
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Check if user already exists
        user = User.query.filter_by(phone_number=phone).first()
        if user:
            flash('Phone number already registered.', 'error')
            return redirect(url_for('auth.signup'))
        
        # Create new user
        new_user = User(phone_number=phone, name=name, role='provider')
        new_user.set_password(password) # Hash the password
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('signup.html')