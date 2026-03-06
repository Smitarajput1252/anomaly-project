from flask_mail import Mail, Message

def send_alert(app, reason):
    mail = Mail(app)

    msg = Message(
        subject="🚨 Critical Health Alert",
        recipients=["admin@gmail.com"],
        body=f"HIGH severity detected.\nReason: {reason}"
    )

    mail.send(msg)