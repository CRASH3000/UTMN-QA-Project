from selenium.webdriver.common.by import By


class FBankLocators:
    BALANCE = (By.ID, "rub-sum")
    RESERVED = (By.ID, "rub-reserved")

    RUB_BLOCK = (By.XPATH, "//h2[text()='Рубли']/ancestor::div[@role='button']")
    USD_BLOCK = (By.XPATH, "//h2[text()='Доллары']/ancestor::div[@role='button']")
    EURO_BLOCK = (By.XPATH, "//h2[text()='Евро']/ancestor::div[@role='button']")

    CARD_INPUT = (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
    SUM_TITLE = (By.XPATH, "//h3[text()='Сумма перевода:']")
    SUM_INPUT = (By.XPATH, "//input[@placeholder='1000']")
    CURRENCY_LABEL = (By.XPATH, "//span[text()='₽' or text()='$' or text()='€']")
    COMMISSION = (By.ID, "comission")
    SUBMIT_BUTTON = (By.XPATH, "//button[.//span[text()='Перевести']]")
    ERROR_MESSAGE = (
        By.XPATH,
        "//span[contains(text(), 'Недостаточно средств на счете')]",
    )
