from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User
from website import db
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Login realizado com sucesso!', category='success')
            return redirect(url_for('admin.painel'))
        else:
            flash('Usuário ou senha incorretos.', category='danger')
            return redirect(url_for('auth.login'))

    return render_template("home.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da conta.', category='info')
    return redirect(url_for('auth.login'))
