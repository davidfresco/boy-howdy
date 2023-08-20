from selenium.webdriver.common.by import By


class Page:

    def __init__(self, driver):
        self._driver = driver

    def scroll_to_bottom(self):
        self._driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    def get_elems(self, xpath):
        elems = self._driver.find_elements(By.XPATH, xpath)
        return elems
