import pytest
from pages.fbank_page import FBankPage
from locators.fbank_locators import FBankLocators


def test_open_start_page(driver):
    page = FBankPage(driver)
    page.open(balance=30000, reserved=20001)

    assert "localhost:8000" in driver.current_url
    assert (
        "balance" in driver.page_source.lower()
        or "reserved" in driver.page_source.lower()
    )


def test_balance_and_reserved_display(driver):
    page = FBankPage(driver)
    balance = 10000
    reserved = 200
    page.open(balance=balance, reserved=reserved)

    assert page.get_balance() == balance
    assert page.get_reserved() == reserved
    assert page.get_reserved() <= page.get_balance()


def test_open_transfer_form_on_rub_click(driver):
    page = FBankPage(driver)
    page.open(balance=10000, reserved=100)

    page.click_currency_block("RUB")

    assert page.is_card_input_visible()


def test_open_transfer_form_on_usd_click(driver):
    page = FBankPage(driver)
    page.open(balance=10000, reserved=100)
    page.click_currency_block("USD")
    assert page.is_card_input_visible()


def test_open_transfer_form_on_eur_click(driver):
    page = FBankPage(driver)
    page.open(balance=10000, reserved=100)
    page.click_currency_block("EUR")
    assert page.is_card_input_visible()


@pytest.mark.parametrize(
    "card_number, expected_visible",
    [
        ("1111 1111 1111 1111", True),  # TC-06
        ("1111 1111 1111 112", False),  # TC-07
        pytest.param(
            "1111 1111 1111 1111 3",
            False,
            marks=pytest.mark.xfail(
                reason="Ожидаемый баг: неверный номер карты не блокирует форму"
            ),
        ),  # TC-08
    ],
)
def test_card_number_validation(driver, card_number, expected_visible):
    page = FBankPage(driver)
    page.open(balance=30000, reserved=20001)

    page.click_currency_block("RUB")
    page.enter_card_number(card_number)

    is_displayed = page.is_transfer_form_displayed()
    assert is_displayed == expected_visible, (
        f"Для номера '{card_number}' ожидалось отображение формы: {expected_visible}, "
        f"но результат: {is_displayed}"
    )


@pytest.mark.parametrize(
    "amount, expected_commission",
    [
        ("10000", 1000.0),  # TC-09
        pytest.param(
            "10",
            1.0,
            marks=pytest.mark.xfail(
                reason="Ожидаемый баг: неправильный расчёт комиссии для малых сумм"
            ),
        ),  # TC-10
        pytest.param(
            "1",
            0.1,
            marks=pytest.mark.xfail(
                reason="Ожидаемый баг: комиссия не отображается для минимальной суммы"
            ),
        ),  # TC-11
    ],
)
def test_commission_calculation(driver, amount, expected_commission):
    page = FBankPage(driver)
    page.open(balance=30000, reserved=20001)

    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")
    assert page.is_transfer_form_displayed(), "Форма перевода не появилась"

    page.enter_transfer_amount(amount)
    actual_commission = page.get_commission_value()

    assert round(actual_commission, 2) == round(
        expected_commission, 2
    ), f"Ожидалась комиссия {expected_commission} ₽, но отображается {actual_commission} ₽"


@pytest.mark.xfail(reason="Ожидаемый баг: поле суммы не ограничивает длину ввода")
def test_transfer_amount_input_length_limit(driver):
    page = FBankPage(driver)
    page.open(balance=999999999, reserved=0)

    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")
    assert page.is_transfer_form_displayed(), "Форма перевода не появилась"

    long_amount = "1" * 30  # Очень длинное число: 30 символов
    page.enter_transfer_amount(long_amount)

    # Проверим, что значение в поле ограничено (например, <= 15 символов)
    amount_input = driver.find_element(*FBankLocators.SUM_INPUT)
    current_value = amount_input.get_attribute("value")

    assert (
        len(current_value) <= 15
    ), f"Поле суммы не ограничивает ввод: длина значения {len(current_value)} символов"

    # Дополнительно: интерфейс не сломался
    assert (
        page.is_transfer_form_displayed()
    ), "Интерфейс пропал после ввода слишком длинной суммы"


@pytest.mark.xfail(reason="Ожидаемый баг: форма принимает отрицательное значение суммы")
def test_negative_transfer_amount(driver):
    page = FBankPage(driver)
    page.open(balance=10000, reserved=0)

    page.click_currency_block("RUB")
    page.enter_card_number("1111 1111 1111 1111")
    assert page.is_transfer_form_displayed(), "Форма перевода не появилась"

    page.enter_transfer_amount("-100")

    # Получаем текущее значение в поле
    amount_input = driver.find_element(*FBankLocators.SUM_INPUT)
    current_value = amount_input.get_attribute("value")

    # Убеждаемся, что оно либо пустое, либо не приняло минус
    assert not current_value.startswith("-"), "Поле приняло отрицательное значение"

    # Проверяем, что кнопка неактивна
    is_enabled = page.is_submit_button_enabled()
    assert (
        not is_enabled
    ), "Кнопка 'Перевести' должна быть неактивна при отрицательном вводе"
