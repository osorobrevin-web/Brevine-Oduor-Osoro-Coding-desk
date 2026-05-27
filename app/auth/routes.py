from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from app.core.utils import generate_id
from app.auth.forms import LoginForm, RegisterForm

# Create the blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        # Redirect authenticated users to their dashboard
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_client():
            return redirect(url_for('client.dashboard'))
        else:
            return redirect(url_for('customer.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('This account has been deactivated.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to role-specific dashboard
        if user.is_admin():
            flash(f'Welcome back, Admin {user.username}!', 'success')
            return redirect(url_for('admin.dashboard'))
        elif user.is_client():
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('client.dashboard'))
        else:
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('customer.dashboard'))
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_client():
            return redirect(url_for('client.dashboard'))
        else:
            return redirect(url_for('customer.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username/email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            id=generate_id(),
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            role=form.role.data,
            is_active=True
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/unauthorized')
def unauthorized():
    """Unauthorized access page"""
    return render_template('auth/unauthorized.html'), 403
