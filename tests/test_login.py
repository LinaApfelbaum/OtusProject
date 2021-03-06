import allure


@allure.title("Login an existing user")
@allure.description("Test checks that an existing user is able to login")
def test_login(user, credentials, inbox_page):
    user.login()
    assert inbox_page.get_logged_user_email() == credentials[0]
