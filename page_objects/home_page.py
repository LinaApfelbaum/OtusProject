from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from framework import get_element


class HomePage:
    EMAIL_FIELD = (By.CSS_SELECTOR, ".email-input")
    DOMAIN_DROPDOWN = (By.CSS_SELECTOR, ".domain-select")
    INPUT_PASSWORD_BUTTON = (
        By.CSS_SELECTOR, "#mailbox button[data-testid='enter-password']")
    PASSWORD_FIELD = (
        By.CSS_SELECTOR, "#mailbox [data-testid='password-input']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "#mailbox [data-testid='login-to-mail']")

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open(self):
        self.browser.get(self.base_url)

    def login(self, credentials):
        login_parts = credentials[0].split('@')
        login = login_parts[0]
        domain = "@" + login_parts[1]

        get_element(self.browser, self.EMAIL_FIELD).send_keys(login)
        Select(self.browser.find_element_by_css_selector(
            ".domain-select")).select_by_value(domain)
        get_element(self.browser, self.INPUT_PASSWORD_BUTTON).click()
        get_element(self.browser, self.PASSWORD_FIELD).send_keys(
            credentials[1])
        get_element(self.browser, self.LOGIN_BUTTON).click()

    def is_logged_in(self):
        try:
            self.browser.find_element_by_css_selector(self.INPUT_PASSWORD_BUTTON[1])
            return False
        except NoSuchElementException:
            return True
