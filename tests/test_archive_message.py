

def test_archive_message(mail, user, inbox_page):
    subject = "Archive me"
    mail.remove_inbox_message(subject)
    mail.create_inbox_message(subject, "body")

    user.login()
    archived_messages_count = inbox_page.archive_message(subject)
    assert archived_messages_count > 0
