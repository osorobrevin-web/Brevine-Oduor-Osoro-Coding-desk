from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.decorators import admin_required
from app.models import User, Event, Ticket, Payout, Review

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_events = Event.query.count()
    total_tickets_sold = Ticket.query.filter_by(status='sold').count()
    total_revenue = db.session.query(db.func.sum(Ticket.price)).filter_by(status='sold').scalar() or 0
    
    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_events=total_events,
                           total_tickets_sold=total_tickets_sold,
                           total_revenue=total_revenue)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Manage all users"""
    page = request.args.get('page', 1, type=int)
    users_paginated = User.query.paginate(page=page, per_page=10)
    return render_template('admin/users.html', users=users_paginated.items, pagination=users_paginated)


@admin_bp.route('/events')
@login_required
@admin_required
def events():
    """View all events"""
    page = request.args.get('page', 1, type=int)
    events_paginated = Event.query.paginate(page=page, per_page=10)
    return render_template('admin/events.html', events=events_paginated.items, pagination=events_paginated)


@admin_bp.route('/tickets')
@login_required
@admin_required
def tickets():
    """View all tickets"""
    page = request.args.get('page', 1, type=int)
    tickets_paginated = Ticket.query.paginate(page=page, per_page=20)
    return render_template('admin/tickets.html', tickets=tickets_paginated.items, pagination=tickets_paginated)


@admin_bp.route('/payouts')
@login_required
@admin_required
def payouts():
    """Manage client payouts"""
    page = request.args.get('page', 1, type=int)
    payouts_paginated = Payout.query.paginate(page=page, per_page=10)
    return render_template('admin/payouts.html', payouts=payouts_paginated.items, pagination=payouts_paginated)


@admin_bp.route('/user/<user_id>/toggle-active')
@login_required
@admin_required
def toggle_user_active(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'User {user.username} status updated.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    """Generate reports"""
    total_revenue = db.session.query(db.func.sum(Ticket.price)).filter_by(status='sold').scalar() or 0
    total_commission = db.session.query(db.func.sum(Ticket.bresca_commission)).filter_by(status='sold').scalar() or 0
    total_mpesa_costs = db.session.query(db.func.sum(Ticket.mpesa_cost)).filter_by(status='sold').scalar() or 0
    total_refunds = db.session.query(db.func.sum(Cancellation.refund_amount)).scalar() or 0
    
    return render_template('admin/reports.html',
                           total_revenue=total_revenue,
                           total_commission=total_commission,
                           total_mpesa_costs=total_mpesa_costs,
                           total_refunds=total_refunds)
