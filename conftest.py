import logging
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from browser_log_listener import BrowserLogListener


def pytest_addoption(parser):
    parser.addoption(
        "--drivers_path", action="store", default="/home/lina/otus/drivers", help="Drivers path"
    )
    parser.addoption(
        "--browser", action="store", default="chrome", help="Select browser from chrome, firefox, opera"
    )
    parser.addoption("--headless", action="store_true", help="Run headless")
    parser.addoption("--executor", action="store",
                     default="127.0.0.1:4444", help="Use 'local' to run tests locally")
    parser.addoption("--browser_version", action="store", default="91.0")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--browser_version")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")

    logger = logging.getLogger('BrowserLogger')
    log_file_handler = logging.FileHandler('logs/browser.log')
    logger.addHandler(log_file_handler)
    logger.setLevel(logging.INFO)

    if executor == "local":
        driver = create_local_driver(request)
    else:
        caps = {
            "browserName": browser_name,
            "browserVersion": version,
            # "screenResolution": "1280x720",
            "name": "Duck",
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": False,
                "enableLog": logs
            },
            # 'acceptSslCerts': True,
            # 'acceptInsecureCerts': True,
            # 'timeZone': 'Europe/Moscow',
            'goog:chromeOptions': {}
        }
        driver = webdriver.Remote(
            command_executor=f"http://{executor}/wd/hub",
            desired_capabilities=caps
        )

    driver = EventFiringWebDriver(driver, BrowserLogListener(logger))

    return driver


def create_local_driver(request):
    drivers_path = request.config.getoption("--drivers_path")
    headless = request.config.getoption("--headless")
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.headless = headless
        driver = webdriver.Chrome(
            executable_path=drivers_path + "/chromedriver", options=options)

    elif browser == "opera":
        if headless:
            raise NotImplementedError("This mode is not supported")

        options = Options()
        driver = webdriver.Opera(
            executable_path=drivers_path + "/operadriver", options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = headless
        driver = webdriver.Firefox(
            executable_path=drivers_path + "/geckodriver", options=options)
    else:
        raise ValueError("Browser is not supported")

    request.addfinalizer(driver.quit)

    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    # execute all other hooks to obtain the report object
    outcome = yield
    result = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "result_" + result.when, result)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(browser, request):
    yield
    if request.node.result_call.failed:
        allure.attach(
            browser.get_screenshot_as_png(),
            name='Screenshot',
            attachment_type=allure.attachment_type.PNG
        )
