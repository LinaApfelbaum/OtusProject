import allure


@allure.title("Empty full Trash folder")
@allure.description("Test checks that full Trash folder is being emptied")
def test_empty_trash(mail, user, inbox_page):
    subject = "Move me to Trash"
    mail.remove_inbox_message(subject)
    mail.create_inbox_message(subject, "body")

    user.login()
    inbox_page.move_to_trash(subject)
    inbox_page.open_trash_folder()
    inbox_page.empty_trash_folder()

    assert "Trash is empty" in inbox_page.get_trash_folder_source()
