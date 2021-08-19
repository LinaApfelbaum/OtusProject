from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_element(driver, locator, timeout=60):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator))


def wait_elements_by(driver, locators, timeout=1):
    WebDriverWait(driver, timeout).until(
        visibility_of_elements(locators)
    )


class visibility_of_elements(object):
    """
    An expectation for checking that all elements are present on the DOM of a
    page and visible.
    """

    def __init__(self, locators):
        self.locators = locators

    def __call__(self, browser):
        try:
            all_elements_are_visible = True
            for locator in self.locators:
                el = EC._find_element(browser, locator)
                is_visible = EC._element_if_visible(el)
                if not is_visible:
                    all_elements_are_visible = False
                    break

            return all_elements_are_visible
        except StaleElementReferenceException:
            return False