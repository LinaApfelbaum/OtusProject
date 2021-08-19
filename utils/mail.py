import poplib
import smtplib
import ssl


class Mail:
    def __init__(self, pop_server, receiver_email, receiver_password,
                 smtp_server, smtp_port, sender_email, sender_password):
        self.sender_password = sender_password
        self.sender_email = sender_email
        self.smtp_port = smtp_port
        self.smtp_server = smtp_server
        self.pop_address = pop_server
        self.receiver_password = receiver_password
        self.receiver_email = receiver_email

    def get_sender_email(self):
        return self.sender_email

    def remove_inbox_message(self, subject):
        mail_server = poplib.POP3_SSL(self.pop_address)
        mail_server.user(self.receiver_email)
        mail_server.pass_(self.receiver_password)
        num_messages = len(mail_server.list()[1])

        for i in range(num_messages):
            letter = mail_server.retr(i + 1)[1]
            for line in letter:
                if line.decode('utf-8') == 'Subject: {}'.format(subject):
                    mail_server.dele(i + 1)

        mail_server.quit()

    def create_inbox_message(self, subject, body):
        message = """\
Subject: {}

{}""".format(subject, body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, message)
