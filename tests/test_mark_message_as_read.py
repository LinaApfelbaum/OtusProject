import allure


@allure.title("Mark an unread message in the Inbox as read")
@allure.description("Test checks that an unread message in the Inbox is being marked as read")
def test_mark_message_as_read(mail, user, inbox_page):
    subject = "Mark me as read"
    mail.remove_inbox_message(subject)
    mail.create_inbox_message(subject, "body")

    user.login()
    read_messages_count = inbox_page.mark_message_as_read(subject)
    assert read_messages_count > 0
