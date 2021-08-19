import logging
import allure
import pytest
from selenium import webdriver
import os.path
from selenium.webdriver.opera.options import Options
from page_objects.home_page import HomePage
from page_objects.inbox_page import InboxPage
from page_objects.settings_folders_page import SettingsFoldersPage
from page_objects.settings_general_page import SettingsGeneralPage
from page_objects.settings_page import SettingsPage
from utils.mail import Mail
from utils.user import User


def pytest_addoption(parser):
    parser.addoption(
        "--drivers_path", action="store", default="/home/lina/otus/drivers", help="Drivers path"
    )
    parser.addoption(
        "--browser", action="store", default="chrome", help="Select browser from chrome, firefox, opera"
    )
    parser.addoption("--headless", action="store_true", help="Run headless")
    parser.addoption("--disable_images", action="store_true", help="Disable images loading")
    parser.addoption("--executor", action="store",
                     default="127.0.0.1:4444", help="Use 'local' to run tests locally")
    parser.addoption("--browser_version", action="store", default="91.0")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--debug_session", action="store_true", default=False)
    parser.addoption("--login", default="otus_test@bk.ru")
    parser.addoption("--password")

    parser.addoption("--pop_server", default="pop.mail.ru")
    parser.addoption("--app_password")
    parser.addoption("--smtp_server", default="smtp.mail.ru")
    parser.addoption("--smtp_port", default="465")
    parser.addoption("--sender_email", default="otus_test_sender@bk.ru")
    parser.addoption("--sender_app_password")


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--browser_version")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    debug_session = request.config.getoption("--debug_session")

    logger = logging.getLogger('BrowserLogger')
    log_file_handler = logging.FileHandler('logs/browser.log')
    logger.addHandler(log_file_handler)
    logger.setLevel(logging.INFO)

    if debug_session and os.path.isfile('debug_session'):
        with open('debug_session') as file:
            debug_data = file.readline().split(' ')
        driver = webdriver.Remote(command_executor=debug_data[1])
        driver.close()
        driver.session_id = debug_data[0]
        return driver

    if executor == "local":
        driver = create_local_driver(request)
    else:
        width = 1366
        height = 768
        caps = {
            "browserName": browser_name,
            "browserVersion": version,
            "screenResolution": f"{width}x{height}x24",
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

        driver.set_window_size(width, height)

    return driver


def create_local_driver(request):
    drivers_path = request.config.getoption("--drivers_path")
    headless = request.config.getoption("--headless")
    disable_images = request.config.getoption("--disable_images")
    browser = request.config.getoption("--browser")
    debug_session = request.config.getoption("--debug_session")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.headless = headless
        options.add_argument("--start-maximized")

        if disable_images:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

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

    if debug_session:
        with open('debug_session', 'w') as file:
            file.write('{} {}'.format(driver.session_id, driver.command_executor._url))
    else:
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


@pytest.fixture()
def user(home_page, credentials, inbox_page):
    return User(home_page, credentials, inbox_page)

@pytest.fixture()
def mail(request):
    return Mail(
        request.config.getoption("--pop_server"),
        request.config.getoption("--login"),
        request.config.getoption("--app_password"),
        request.config.getoption("--smtp_server"),
        int(request.config.getoption("--smtp_port")),
        request.config.getoption("--sender_email"),
        request.config.getoption("--sender_app_password"))

@pytest.fixture()
def base_url():
    return "https://mail.ru"

@pytest.fixture()
def inbox_base_url():
    return "https://e.mail.ru/inbox/"

@pytest.fixture()
def credentials(request):
    return (request.config.getoption("--login"), request.config.getoption("--password"))

@pytest.fixture()
def home_page(browser, base_url):
    return HomePage(browser, base_url)

@pytest.fixture()
def inbox_page(browser, inbox_base_url):
    return InboxPage(browser, inbox_base_url)

@pytest.fixture()
def settings_page(browser):
    return SettingsPage(browser)

@pytest.fixture()
def settings_general_page(browser):
    return SettingsGeneralPage(browser)

@pytest.fixture()
def settings_folders_page(browser):
    return SettingsFoldersPage(browser)
