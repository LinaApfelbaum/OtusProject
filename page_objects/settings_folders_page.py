import time

from selenium.webdriver.common.by import By

from framework import get_element


class SettingsFoldersPage:
    ADD_FOLDER_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='create']")
    DIALOG_FOLDER_NAME_FIELD = (By.CSS_SELECTOR, "input[data-test-id='name']")
    DIALOG_FOLDER_ADD_BUTTON = (
        By.CSS_SELECTOR, "button[data-test-id='submit']")

    DELETE_FOLDER_BUTTON = "button[data-test-id='folder-delete']"
    CONFIRMATION_DELETE_BUTTON = (
        By.CSS_SELECTOR, "button[data-test-id='submit']")

    FOLDER_NAME = "[data-test-id='folder-name']"
    ALL_FOLDERS = "[data-test-id^='folder:']"

    def __init__(self, browser):
        self.browser = browser

    def create_folder(self, name):
        get_element(self.browser, self.ADD_FOLDER_BUTTON).click()
        get_element(self.browser, self.DIALOG_FOLDER_NAME_FIELD).send_keys(name)
        get_element(self.browser, self.DIALOG_FOLDER_ADD_BUTTON).click()
        get_element(self.browser, (By.XPATH,
                    "//*[@data-test-id='folder-name'][contains(text(),'{}')]".format(name)))

    def get_all_folders(self):
        folders_list = []

        for element in self._find_folder_elements():
            folder_name_element = element.find_element_by_css_selector(
                self.FOLDER_NAME)
            folders_list.append(folder_name_element.text)

        return folders_list

    def delete_folder(self, name):
        for element in self._find_folder_elements():
            folder_name_element = element.find_element_by_css_selector(
                self.FOLDER_NAME)
            if folder_name_element.text == name:
                element.find_element_by_css_selector(
                    self.DELETE_FOLDER_BUTTON).click()
                get_element(
                    self.browser, self.CONFIRMATION_DELETE_BUTTON).click()
        time.sleep(1)

    def _find_folder_elements(self):
        get_element(self.browser, (By.CSS_SELECTOR, self.ALL_FOLDERS))
        return self.browser.find_elements_by_css_selector(self.ALL_FOLDERS)
