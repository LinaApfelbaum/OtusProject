

class User:
    def __init__(self, home_page, credentials, inbox_page):
        self.inbox_page = inbox_page
        self.credentials = credentials
        self.home_page = home_page

    def login(self):
        self.home_page.open()

        if self.home_page.is_logged_in():
            self.inbox_page.open()
        else:
            self.home_page.login(self.credentials)
