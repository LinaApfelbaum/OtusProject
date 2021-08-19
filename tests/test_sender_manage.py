import allure


@allure.title("Manage senders in the Settings")
@allure.description("Test checks senders are being created and deleted")
def test_sender_manage(user, inbox_page, settings_page, settings_general_page):
    sender_name = "test_name"
    sender_signature = "test_signature"

    user.login()
    inbox_page.open_all_settings()
    settings_page.open_general_page()
    settings_general_page.create_sender(sender_name, sender_signature)

    senders = settings_general_page.get_all_senders()
    assert sender_name in senders

    settings_general_page.delete_sender(sender_name)

    senders = settings_general_page.get_all_senders()
    settings_general_page.close_tab()
    assert sender_name not in senders
