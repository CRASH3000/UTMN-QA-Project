import pytest
from selenium.common import TimeoutException, NoSuchElementException


@pytest.mark.xfail(
    reason="Ожидаемый баг: при пустом поле появляется ошибка 'Недостаточно средств'",
    strict=True,
)
def test_no_error_when_amount_field_is_empty(driver):
    page = FBankPage(driver)
    page.open(balance=1000, reserved=0)
    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")

    page.enter_transfer_amount("")

    assert page.get_transfer_amount_value() == "", "Поле суммы должно быть пустым"

    try:
        error_elem = driver.find_element(*FBankLocators.ERROR_MESSAGE)
        assert (
            False
        ), f"Ошибка 'Недостаточно средств' не должна отображаться при пустом поле, но была: '{error_elem.text}'"
    except NoSuchElementException:
        pass


@pytest.mark.xfail(
    reason="Ожидаемый баг: отображается отрицательный баланс", strict=True
)
def test_negative_balance_via_url(driver):
    page = FBankPage(driver)
    page.open(balance=-1000, reserved=0)

    displayed_balance = page.get_balance()
    assert (
        displayed_balance >= 0
    ), f"Баланс не должен быть отрицательным, но отображается: {displayed_balance}"


from pages.fbank_page import FBankPage
from locators.fbank_locators import FBankLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_small_amount_transfer_is_possible(driver):
    page = FBankPage(driver)
    page.open(balance=100, reserved=0)
    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_transfer_amount("10")

    assert (
        page.is_submit_button_enabled()
    ), "Кнопка 'Перевести' должна быть доступна при переводе 10₽"

    error_elements = driver.find_elements(*FBankLocators.ERROR_MESSAGE)
    visible_errors = [e.text for e in error_elements if e.is_displayed()]
    assert (
        not visible_errors
    ), f"Не должно быть ошибок, но отображаются: {visible_errors}"
    page.submit_transfer()

    alert_text = page.get_alert_text_and_accept()
    assert alert_text is not None, "Окно подтверждения не появилось"
    assert "принят банком" in alert_text.lower(), f"Неверный текст алерта: {alert_text}"


def test_full_balance_transfer_is_blocked(driver):
    page = FBankPage(driver)
    page.open(balance=10000, reserved=0)
    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_transfer_amount("10000")

    assert (
        not page.is_submit_button_enabled()
    ), "Кнопка 'Перевести' не должна быть активна при превышении баланса"

    error_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(FBankLocators.ERROR_MESSAGE)
    )
    assert (
        "недостаточно средств" in error_elem.text.lower()
    ), f"Ожидалась ошибка 'Недостаточно средств на счете', но было: '{error_elem.text}'"


@pytest.mark.xfail(
    reason="Ожидаемый баг: кнопка активна при превышении баланса в валютном переводе (USD)",
    strict=True,
)
def test_full_usd_balance_transfer_is_blocked(driver):
    page = FBankPage(driver)
    page.open(balance=10000, reserved=0)  # баланс в рублях
    page.click_currency_block("USD")
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_transfer_amount("100")  # 100 USD + комиссия

    assert (
        not page.is_submit_button_enabled()
    ), "Кнопка 'Перевести' не должна быть активна при превышении доступного рублёвого баланса"

    error_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(FBankLocators.ERROR_MESSAGE)
    )
    assert (
        "недостаточно средств" in error_elem.text.lower()
    ), f"Ожидалась ошибка 'Недостаточно средств на счете', но текст: '{error_elem.text}'"


@pytest.mark.xfail(
    reason="Ожидаемый баг: кнопка активна при превышении баланса в валютном переводе (EUR)",
    strict=True,
)
def test_full_eur_balance_transfer_is_blocked(driver):
    page = FBankPage(driver)
    page.open(balance=10000, reserved=0)  # баланс в рублях
    page.click_currency_block("EUR")
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_transfer_amount("100")  # 100 USD + комиссия

    assert (
        not page.is_submit_button_enabled()
    ), "Кнопка 'Перевести' не должна быть активна при превышении доступного рублёвого баланса"

    error_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(FBankLocators.ERROR_MESSAGE)
    )
    assert (
        "недостаточно средств" in error_elem.text.lower()
    ), f"Ожидалась ошибка 'Недостаточно средств на счете', но текст: '{error_elem.text}'"
