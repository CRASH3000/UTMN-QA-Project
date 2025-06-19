import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.fbank_page import FBankPage

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def prepared_rub_transfer(driver):
    def _transfer(amount):
        page = FBankPage(driver)
        page.open(balance=30000, reserved=20001)
        page.click_currency_block("RUB")
        page.enter_card_number("1111 1111 1111 1111")
        page.enter_transfer_amount(str(amount))
        return page
    return _transfer