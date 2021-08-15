
def test_send_message(user, mail, inbox_page):
    recipient_email = mail.get_sender_email()
    subject = "test_subject"
    body = "Test body"

    user.login()
    confirmation_text = inbox_page.send_message(recipient_email, subject, body)

    assert "Message sent" in confirmation_text
    # assert "To: <{}>".format(recipient_email) in confirmation_text
