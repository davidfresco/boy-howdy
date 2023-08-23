import time
import pickle
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from reddit.pages.homepage import Homepage
from reddit.pages.subreddit import Subreddit


class Reddit:

    LOGIN_COOKIES = ["loid", "token_v2" "csv", "edgebucket", "reddit_session",
                     "session_tracker", "token_v2", "wwrbucket"]
    COOKIES_FILE = "cookies.pkl"

    def __init__(self, username=None, password=None, cookies=None,
                 headless=True):
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        if headless:
            options.add_argument("--headless")
        self._driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            chrome_options=options)
        self._driver.get("https://www.reddit.com/login")
        try:
            if cookies is None:
                cookies = pickle.load(open(self.COOKIES_FILE, "rb"))
            for cookie in cookies:
                if cookie["name"] in self.LOGIN_COOKIES:
                    self._driver.add_cookie(cookie)
            self.logged_in = True
        except Exception:
            self.login(username, password)
        self._pages = {
            "homepage": Homepage,
            "subreddit": Subreddit
        }
        self._current_page = Homepage(self._driver)

    def set_page(self, page_type, page_data=None):
        new_page = self._pages[page_type](self._driver, page_data)
        self._current_page = new_page
        self._current_page_type = page_type

    def first_page(self):
        data = self._current_page.first_page()
        return data

    def next_page(self):
        data = self._current_page.next_page()
        return data

    def _get_elem(self, xpath):
        elem = self._driver.find_element(By.XPATH, xpath)
        return elem

    def login(self, username, password):
        if username is None or password is None:
            # raise Exception("no credentials supplied for login")
            print("remaining logged out")
            self.logged_in = False
            return
        print("logging in...")
        self._driver.get("https://www.reddit.com/login")
        username_field = self._get_elem("//input[@id='loginUsername']")
        password_field = self._get_elem("//input[@id='loginPassword']")
        login_button = self._get_elem("//button[contains(text(), 'Log In')]")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(1)
        pickle.dump(self._driver.get_cookies(), open(self.COOKIES_FILE, "wb"))
        self.logged_in = True
        print("logged in")
