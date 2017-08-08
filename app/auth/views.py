from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
    current_app, )
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin.contrib.sqla import ModelView

from ..models import User
from .. import db
from ..email import send_email
from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Usuário ou password inválido(s).')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log Out realizado com sucesso.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(
            user.email,
            'Confirme sua conta',
            'auth/email/confirm',
            user=user,
            token=token)
        flash('Uma mensagem de confirmação foi enviado para seu email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Conta verificada. Obrigado!')
    else:
        flash('O link de confirmação não é válido ou expirou.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(
        current_user.email,
        'Confirme sua conta',
        'auth/email/confirm',
        user=current_user,
        token=token)
    flash('Uma nova mensagem de confirmação foi enviada ao seu email.')
    return redirect(url_for('main.index'))


class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator(
        )

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))
