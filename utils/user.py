

class User:
    def __init__(self, home_page, credentials):
        self.credentials = credentials
        self.home_page = home_page

    def login(self):
        self.home_page.open()
        self.home_page.login(self.credentials)
