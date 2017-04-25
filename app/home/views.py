from flask import render_template
from flask_login import login_required, current_user

from . import home


@home.route('/')
def homepage():

    return render_template('home/index.html', title='Welcome to Squad Master')

@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title='Admin Dashboard')
