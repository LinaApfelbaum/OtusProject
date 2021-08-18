import allure

@allure.title("Manage folders in the Settings")
@allure.description("Test checks folders are being created and deleted")
def test_folder_manage(user, inbox_page, settings_page, settings_folders_page):
    folder_name = "test_name"

    user.login()
    inbox_page.open_all_settings()
    settings_page.open_folders_page()
    settings_folders_page.create_folder(folder_name)

    folders = settings_folders_page.get_all_folders()
    assert folder_name in folders

    settings_folders_page.delete_folder(folder_name)

    folders = settings_folders_page.get_all_folders()
    assert folder_name not in folders
