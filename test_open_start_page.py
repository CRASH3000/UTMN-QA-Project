import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_open_start_page(driver):
    url = "http://localhost:8000/?balance=30000&reserved=20001"
    driver.get(url)

    # Простейшая проверка: страница открыта, заголовок или элемент есть
    assert (
        "http://localhost:8000" in driver.current_url
    ), "Стартовая страница не открылась"

    # Можно добавить проверку контента на странице:
    assert (
        "balance" in driver.page_source.lower()
        or "reserved" in driver.page_source.lower()
    )


def test_balance_and_reserve_display(driver):
    balance = 10000
    reserved = 200
    url = f"http://localhost:8000/?balance={balance}&reserved={reserved}"

    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # Явное ожидание появления элементов
    balance_elem = wait.until(EC.visibility_of_element_located((By.ID, "rub-sum")))
    reserve_elem = wait.until(EC.visibility_of_element_located((By.ID, "rub-reserved")))

    # Получаем значения со страницы
    balance_text = balance_elem.text.replace("'", "").replace(" ", "")
    reserve_text = reserve_elem.text.replace("'", "").replace(" ", "")

    # Переводим в числа
    balance_value = int(balance_text)
    reserve_value = int(reserve_text)

    # Проверки
    assert (
        balance_value == balance
    ), f"Ожидался баланс {balance}, но на странице {balance_value}"
    assert (
        reserve_value == reserved
    ), f"Ожидался резерв {reserved}, но на странице {reserve_value}"
    assert reserve_value <= balance_value, "Резерв не должен превышать счёт"
