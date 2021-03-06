import allure


@allure.title("Find a message in the Inbox")
@allure.description("Test checks that user is able to search the Inbox")
def test_search_inbox(mail, user, inbox_page):
    subject = "Find me"
    mail.remove_inbox_message(subject)
    mail.create_inbox_message(subject, "body")

    user.login()
    inbox_page.search(subject)
    messages_subjects = inbox_page.get_messages_subjects()
    assert [subject] == messages_subjects
