from selenium.webdriver.common.by import By

from framework import get_element


class SettingsPage:
    SETTINGS_GENERAL_LINK = (
        By.CSS_SELECTOR, "[data-test-id='navigation-menu-body'] [data-test-id='navigation-menu-item:general']")
    SETTINGS_FOLDERS_LINK = (
        By.CSS_SELECTOR, "[data-test-id='navigation-menu-body'] [data-test-id='navigation-menu-item:folders']")

    def __init__(self, browser):
        self.browser = browser

    def open_general_page(self):
        get_element(self.browser, self.SETTINGS_GENERAL_LINK).click()

    def open_folders_page(self):
        get_element(self.browser, self.SETTINGS_FOLDERS_LINK).click()
