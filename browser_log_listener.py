from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


class BrowserLogListener(AbstractEventListener):
    def __init__(self, logger):
        self.logger = logger

    def before_navigate_to(self, url, driver):
        self.logger.info(f"I'm navigating to {url} and {driver.title}")

    def after_navigate_to(self, url, driver):
        self.logger.info(f"I'm on {url}")

    def before_navigate_back(self, driver):
        self.logger.info("I'm navigating back")

    def after_navigate_back(self, driver):
        self.logger.info("I'm back!")

    def before_find(self, by, value, driver):
        self.logger.info(f"I'm looking for '{value}' with '{by}'")

    def after_find(self, by, value, driver):
        self.logger.info(f"I've found '{value}' with '{by}'")

    def before_click(self, element, driver):
        self.logger.info(f"I'm clicking {element}")

    def after_click(self, element, driver):
        self.logger.info(f"I've clicked {element}")

    def before_execute_script(self, script, driver):
        self.logger.info(f"I'm executing '{script}'")

    def after_execute_script(self, script, driver):
        self.logger.info(f"I've executed '{script}'")

    def before_quit(self, driver):
        self.logger.info(f"I'm getting ready to terminate {driver}")

    def after_quit(self, driver):
        self.logger.info("Browser closed")

    def on_exception(self, exception, driver):
        self.logger.error(f"Oops i got: {exception}")
        driver.save_screenshot(f'logs/{exception}.png')
