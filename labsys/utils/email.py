from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from ..extensions import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(recipients, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        subject=app.config['LABSYS_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=app.config['LABSYS_MAIL_SENDER'],
        recipients=recipients,
        charset='utf-8')
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
