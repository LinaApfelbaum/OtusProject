from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


from framework.framework import get_element


class InboxPage:
    USER_PANEL = (By.CSS_SELECTOR, ".ph-project__account")
    USER_PANEL_EMAIL = (By.CSS_SELECTOR, ".ph-project__user-name")
    EXIT_LINK = (By.CSS_SELECTOR, ".ph-sidebar a[href*='logout']")

    COMPOSE_MESSAGE_BUTTON = (By.CSS_SELECTOR, ".sidebar [title='Compose']")
    RECIPIENT_FIELD = (
        By.CSS_SELECTOR, ".compose-app__compose [data-name='to'] input")
    SUBJECT_FIELD = (
        By.CSS_SELECTOR, ".compose-app__compose input[name='Subject']")
    EDITOR_BODY_BOX = (
        By.CSS_SELECTOR, "[role='textbox'][contenteditable='true']")
    SEND_MESSAGE_BUTTON = (
        By.CSS_SELECTOR, ".compose-app__buttons [title='Send']")

    DELETE_MESSAGE_BUTTON = (
        By.CSS_SELECTOR, ".portal-menu-element [title='Delete']")
    MARK_AS_READ_BUTTON = (
        By.CSS_SELECTOR, ".portal-menu-element [title='Read']")

    SEARCH_PANEL_FIELD = (
        By.CSS_SELECTOR, ".search-panel__right-col .search-panel-button")
    SEARCH_PANEL_INPUT = (By.CSS_SELECTOR, ".search-panel__layer input")
    SEARCH_PANEL_BUTTON = (
        By.XPATH, "//*[@class='search-panel__layer']//*[contains(text(),'Search')]")
    SEARCH_RESULT_TOP = (By.CSS_SELECTOR, ".list-letter-preview-action")

    SETTINGS_BUTTON = (
        By.CSS_SELECTOR, ".sidebar__bottom-menu [title='Settings']")
    SETTINGS_PANEL_LINK = (By.CSS_SELECTOR, "a[href*='settings']")

    CONFIRMATION_CONTAINER = (By.CSS_SELECTOR, ".layer-window__container")

    ALL_MESSAGES = ".js-tooltip-direction_letter-bottom"
    MESSAGE_CHECKBOX = ".checkbox__label"
    MESSAGES_PANEL_ACTIONS = (
        By.CSS_SELECTOR, ".portal-menu-element .dropdown-actions")
    MARK_AS_READ_ACTION = (
        By.CSS_SELECTOR, ".dropdown__menu .list-item__ico_read")
    ARCHIVE_ACTION = (By.CSS_SELECTOR, ".portal-menu-element_archive")
    DELETE_ACTION = (By.CSS_SELECTOR, ".portal-menu-element_remove")
    MOVE_TO_ACTION = (By.CSS_SELECTOR, ".dropdown [title='Move to']")
    MOVE_TO_TRASH_FOLDER = (
        By.CSS_SELECTOR, ".list-nested-moveto-folder [title='Trash']")

    TRASH_FOLDER = (By.CSS_SELECTOR, "#sideBarContent [title^='Trash']")
    EMPTY_FOLDER_LINK = (By.CSS_SELECTOR, ".list-letter-tip a.link")
    CONFIRMATION_EMPTY_BUTTON = (By.CSS_SELECTOR, ".layer__submit-button")
    EMPTY_TRASH_TEXT = (By.CSS_SELECTOR, ".octopus__title")

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open(self):
        self.browser.get(self.base_url)

    def get_logged_user_email(self):
        return get_element(self.browser, self.USER_PANEL_EMAIL).text.strip()

    def logout(self):
        get_element(self.browser, self.USER_PANEL).click()
        get_element(self.browser, self.EXIT_LINK).click()

    def open_all_settings(self):
        get_element(self.browser, self.SETTINGS_BUTTON, timeout=60).click()
        get_element(self.browser, self.SETTINGS_PANEL_LINK).click()
        self.browser.switch_to.window(self.browser.window_handles[1])

    def send_message(self, recipient_email, subject, body):
        get_element(self.browser, self.COMPOSE_MESSAGE_BUTTON).click()
        get_element(self.browser, self.RECIPIENT_FIELD).send_keys(
            recipient_email)
        get_element(self.browser, self.SUBJECT_FIELD).send_keys(subject)
        get_element(self.browser, self.EDITOR_BODY_BOX).send_keys(body)
        get_element(self.browser, self.SEND_MESSAGE_BUTTON).click()

        return get_element(self.browser, self.CONFIRMATION_CONTAINER).text

    def mark_message_as_read(self, subject):
        count_of_read_messages = 0
        for element in self._find_all_messages():
            if subject in element.text:
                action = ActionChains(self.browser)
                checkbox = element.find_element_by_css_selector(
                    self.MESSAGE_CHECKBOX)
                action.move_to_element(checkbox)
                action.perform()
                checkbox.click()
                get_element(self.browser, self.MESSAGES_PANEL_ACTIONS).click()
                get_element(self.browser, self.MARK_AS_READ_ACTION).click()
                count_of_read_messages += 1

        return count_of_read_messages

    def archive_message(self, subject):
        count_of_archived_messages = 0
        for element in self._find_all_messages():
            if subject in element.text:
                action = ActionChains(self.browser)
                checkbox = element.find_element_by_css_selector(
                    self.MESSAGE_CHECKBOX)
                action.move_to_element(checkbox)
                action.perform()
                checkbox.click()
                get_element(self.browser, self.ARCHIVE_ACTION).click()
                count_of_archived_messages += 1

        return count_of_archived_messages

    def delete_message(self, subject):
        count_of_deleted_messages = 0
        for element in self._find_all_messages():
            if subject in element.text:
                action = ActionChains(self.browser)
                checkbox = element.find_element_by_css_selector(
                    self.MESSAGE_CHECKBOX)
                action.move_to_element(checkbox)
                action.perform()
                checkbox.click()
                get_element(self.browser, self.DELETE_ACTION).click()
                count_of_deleted_messages += 1

        return count_of_deleted_messages

    def search(self, subject):
        get_element(self.browser, self.SEARCH_PANEL_FIELD).click()
        get_element(self.browser, self.SEARCH_PANEL_INPUT).send_keys(subject)
        get_element(self.browser, self.SEARCH_PANEL_BUTTON).click()
        get_element(self.browser, self.SEARCH_RESULT_TOP)

    def get_messages_subjects(self):
        subjects = []
        for element in self._find_all_messages():
            subject_element = element.find_element_by_css_selector(
                ".highlighter")
            subjects.append(subject_element.text)
        return subjects

    def move_to_trash(self, subject):
        for element in self._find_all_messages():
            if subject in element.text:
                action = ActionChains(self.browser)
                checkbox = element.find_element_by_css_selector(
                    self.MESSAGE_CHECKBOX)
                action.move_to_element(checkbox)
                action.perform()
                checkbox.click()
                get_element(self.browser, self.MOVE_TO_ACTION).click()
                get_element(self.browser, self.MOVE_TO_TRASH_FOLDER).click()

    def open_trash_folder(self):
        get_element(self.browser, self.TRASH_FOLDER).click()

    def empty_trash_folder(self):
        get_element(self.browser, self.EMPTY_FOLDER_LINK).click()
        get_element(self.browser, self.CONFIRMATION_EMPTY_BUTTON).click()
        get_element(self.browser, self.EMPTY_TRASH_TEXT)

    def get_trash_folder_source(self):
        return get_element(self.browser, (By.CSS_SELECTOR, 'html')).text

    def _find_all_messages(self):
        get_element(self.browser, (By.CSS_SELECTOR,
                    self.ALL_MESSAGES), timeout=60)
        return self.browser.find_elements_by_css_selector(self.ALL_MESSAGES)
