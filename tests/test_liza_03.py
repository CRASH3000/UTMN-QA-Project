import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.fbank_locators import FBankLocators
from pages.fbank_page import FBankPage


def test_card_field_rejects_letters(driver):
    page = FBankPage(driver)
    page.open()
    page.click_currency_block("RUB")
    page.enter_card_number("abcd efgh ijkl №%mn")

    card_input_value = page.get_card_input_value()
    assert card_input_value == "", f"Поле должно быть пустым, но содержит: '{card_input_value}'"


import pytest

@pytest.mark.parametrize("balance, reserved, amount, expected_error", [
    (0, 0, 1, "недостаточно средств"),           # TC-22: Пустой счёт
    (100, 0, 95, "недостаточно средств"),        # TC-23: Сумма + комиссия > счёта
    (2000, 2000, 10, "недостаточно средств"),    # TC-24: Счёт = резерв
])
def test_transfer_blocked_due_to_insufficient_funds(driver, balance, reserved, amount, expected_error):
    page = FBankPage(driver)
    page.open(balance=balance, reserved=reserved)
    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_transfer_amount(str(amount))

    assert not page.is_submit_button_enabled(), "Кнопка 'Перевести' не должна быть активна"

    error_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(FBankLocators.ERROR_MESSAGE)
    )
    assert expected_error in error_elem.text.lower(), (f"Ожидалась ошибка: '{expected_error}', "
                                                       f"но текст: '{error_elem.text}'")


def test_leading_zero_in_amount_field(driver):
    page = FBankPage(driver)
    page.open(balance=1000, reserved=0)
    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")

    page.enter_transfer_amount("0444")
    amount_value = page.get_transfer_amount_value()


    error_elements = driver.find_elements(*FBankLocators.ERROR_MESSAGE)
    is_button_enabled = page.is_submit_button_enabled()

    assert amount_value == "444" or error_elements or not is_button_enabled, (
        f"Ожидалась автоочистка ведущего нуля, сообщение об ошибке или неактивная кнопка.\n"
        f"Текущее значение суммы: {amount_value}, ошибок: {len(error_elements)}, кнопка активна: {is_button_enabled}"
    )

def test_zero_amount_transfer_is_blocked(driver):
    page = FBankPage(driver)
    page.open(balance=1000, reserved=0)
    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")

    page.enter_transfer_amount("0")
    assert not page.is_submit_button_enabled(), "Кнопка 'Перевести' не должна быть активна при сумме 0₽"