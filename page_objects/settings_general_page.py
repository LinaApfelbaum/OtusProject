import time

from selenium.webdriver.common.by import By

from framework import get_element


class SettingsGeneralPage:
    ADD_SENDER_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='create']")
    DIALOG_SENDER_NAME_FIELD = (
        By.CSS_SELECTOR, "input[data-test-id='name_input']")
    DIALOG_SENDER_SIGNATURE_FIELD = (
        By.CSS_SELECTOR, "[data-test-id='signature-create-popup'] [role='textbox']")
    DIALOG_SENDER_ADD_BUTTON = (
        By.CSS_SELECTOR, "[data-test-id='signature-create-popup'] button[data-test-id='save']")

    DELETE_SENDER_BUTTON = "[data-test-id='remove']"
    CONFIRMATION_DELETE_BUTTON = (
        By.CSS_SELECTOR, "[data-test-id$='-delete-popup'] button[data-test-id='delete']")

    ALL_SENDERS = "[data-test-id^='signature:']"
    SENDER_NAME = "[data-test-id='name']"

    def __init__(self, browser):
        self.browser = browser

    def create_sender(self, name, signature):
        get_element(self.browser, self.ADD_SENDER_BUTTON).click()
        get_element(self.browser, self.DIALOG_SENDER_NAME_FIELD).send_keys(name)
        get_element(self.browser, self.DIALOG_SENDER_SIGNATURE_FIELD).send_keys(
            signature)
        get_element(self.browser, self.DIALOG_SENDER_ADD_BUTTON).click()

    def get_all_senders(self):
        senders_list = []

        for element in self._find_sender_elements():
            sender_name_element = element.find_element_by_css_selector(
                self.SENDER_NAME)
            senders_list.append(sender_name_element.text)

        return senders_list

    def delete_sender(self, name):
        for element in self._find_sender_elements():
            sender_name_element = element.find_element_by_css_selector(
                self.SENDER_NAME)
            if sender_name_element.text == name:
                element.find_element_by_css_selector(
                    self.DELETE_SENDER_BUTTON).click()
                get_element(
                    self.browser, self.CONFIRMATION_DELETE_BUTTON).click()
        time.sleep(1)

    def close_tab(self):
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def _find_sender_elements(self):
        get_element(self.browser, (By.CSS_SELECTOR, self.ALL_SENDERS))
        return self.browser.find_elements_by_css_selector(self.ALL_SENDERS)
