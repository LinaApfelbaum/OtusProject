import allure


@allure.title("Logout user from the Inbox page")
@allure.description("Test checks that user is able to logout from the Inbox page")
def test_logout(user, inbox_page, browser):
    user.login()
    inbox_page.logout()

    assert "logout" in browser.current_url
