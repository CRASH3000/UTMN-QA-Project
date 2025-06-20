import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.fbank_locators import FBankLocators
from pages.fbank_page import FBankPage


def test_successful_rub_transfer_alert(prepared_rub_transfer):
    page = prepared_rub_transfer(100)
    page.submit_transfer()
    alert_text = page.get_alert_text_and_accept()
    assert alert_text is not None, "Окно подтверждения не появилось"
    assert "принят банком" in alert_text.lower(), f"Неверный текст алерта: {alert_text}"


@pytest.mark.xfail(reason="Ожидаемый баг: баланс не изменяется после перевода")
def test_balance_after_rub_transfer(prepared_rub_transfer):
    amount = 100
    commission = int(amount * 0.1)
    expected_balance = 30000 - amount - commission

    page = prepared_rub_transfer(amount)
    page.submit_transfer()
    page.get_alert_text_and_accept()

    new_balance = page.get_balance()
    assert (
        new_balance == expected_balance
    ), f"Ожидалось: {expected_balance}, получено: {new_balance}"


@pytest.mark.parametrize(
    "amount, error_text",
    [
        ("100000", "недостаточно средств на счете"),  # TC-16
        pytest.param(
            "-100",
            "недостаточно средств на счете",
            marks=pytest.mark.xfail(
                reason="Ожидаемый баг: кнопка 'Перевести' активна при отрицательной сумме"
            ),
            id="TC-17",
        ),
    ],
)  # TC-17
def test_transfer_blocked_on_invalid_amount(prepared_rub_transfer, amount, error_text):
    page = prepared_rub_transfer(amount)

    assert (
        not page.is_submit_button_enabled()
    ), "Кнопка 'Перевести' должна быть неактивна при некорректной сумме"

    error_element = WebDriverWait(page.driver, 5).until(
        EC.visibility_of_element_located(FBankLocators.ERROR_MESSAGE)
    )
    actual_text = error_element.text.strip().lower()
    assert (
        error_text in actual_text
    ), f"Ожидалась ошибка: '{error_text}', но было: '{actual_text}'"


@pytest.mark.xfail(reason="Ожидаемый баг: неверное округление комиссии")
def test_commission_rounding_down(prepared_rub_transfer):
    page = prepared_rub_transfer(999)
    commission_text = page.get_commission_value()
    assert (
        commission_text == "99 ₽"
    ), f"Ожидалась комиссия 99 ₽, но отображается: {commission_text}"


def test_transfer_blocked_when_balance_equals_reserved(driver):
    page = FBankPage(driver)
    page.open(balance=200, reserved=200)
    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_transfer_amount("50")

    assert (
        not page.is_submit_button_enabled()
    ), "Кнопка 'Перевести' должна быть неактивна при недоступных средствах"

    error_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(FBankLocators.ERROR_MESSAGE)
    )
    assert (
        "недостаточно средств" in error_element.text.lower()
    ), f"Ожидалась ошибка о нехватке средств, но было: {error_element.text}"
