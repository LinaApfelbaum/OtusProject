

def test_archive_message(mail, user, inbox_page):
    subject = "Delete me"
    mail.remove_inbox_message(subject)
    mail.create_inbox_message(subject, "body")

    user.login()
    deleted_messages_count = inbox_page.delete_message(subject)
    assert deleted_messages_count > 0
