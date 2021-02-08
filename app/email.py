from threading import Thread
from flask_mail import Message
from flask import render_template
from app import mail, app


# step 102 in the workflow
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)

    # step 102 in the workflow
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    # step 98 in the workflow
    token = user.get_reset_password()
    send_email(
        subject="[Microblog] reset your password",
        sender=app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )
