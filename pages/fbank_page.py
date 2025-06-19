from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.fbank_locators import FBankLocators
from selenium.common.exceptions import TimeoutException

class FBankPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, balance=0, reserved=0):
        url = f"http://localhost:8000/?balance={balance}&reserved={reserved}"
        self.driver.get(url)

    def get_balance(self):
        elem = self.wait.until(EC.visibility_of_element_located(FBankLocators.BALANCE))
        return int(elem.text.replace("'", "").replace(" ", ""))

    def get_reserved(self):
        elem = self.wait.until(EC.visibility_of_element_located(FBankLocators.RESERVED))
        return int(elem.text.replace("'", "").replace(" ", ""))

    def click_currency_block(self, currency: str):
        locator_map = {
            "RUB": FBankLocators.RUB_BLOCK,
            "USD": FBankLocators.USD_BLOCK,
            "EUR": FBankLocators.EURO_BLOCK
        }
        block = self.wait.until(EC.element_to_be_clickable(locator_map[currency]))
        block.click()

    def is_card_input_visible(self):
        return self.wait.until(EC.visibility_of_element_located(FBankLocators.CARD_INPUT))

    def get_card_input_value(self):
        return self.driver.find_element(*FBankLocators.CARD_INPUT).get_attribute("value")

    def is_card_input_invalid(self):
        card_input = self.driver.find_element(*FBankLocators.CARD_INPUT)
        return "error" in card_input.get_attribute("class")

    def enter_card_number(self, number: str):
        input_field = self.wait.until(EC.visibility_of_element_located(FBankLocators.CARD_INPUT))
        input_field.clear()
        input_field.send_keys(number)

    def is_transfer_form_displayed(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(FBankLocators.SUM_TITLE))
            self.wait.until(EC.visibility_of_element_located(FBankLocators.SUM_INPUT))
            self.wait.until(EC.visibility_of_element_located(FBankLocators.CURRENCY_LABEL))
            self.wait.until(EC.visibility_of_element_located(FBankLocators.COMMISSION))
            self.wait.until(EC.visibility_of_element_located(FBankLocators.SUBMIT_BUTTON))
            return True
        except:
            return False

    def enter_transfer_amount(self, amount: str):
        amount_input = self.wait.until(EC.visibility_of_element_located(FBankLocators.SUM_INPUT))
        amount_input.clear()
        amount_input.send_keys(amount)

    def get_commission_value(self) -> float:
        commission_elem = self.wait.until(EC.visibility_of_element_located(FBankLocators.COMMISSION))
        text = commission_elem.text.replace(",", ".").replace("₽", "").strip()
        return float(text)

    def is_submit_button_enabled(self):
        buttons = self.driver.find_elements(*FBankLocators.SUBMIT_BUTTON)
        if not buttons:
            return False  # Кнопка отсутствует в DOM
        return buttons[0].is_enabled()  # Кнопка есть, проверим активность

    def submit_transfer(self):
        button = self.wait.until(EC.element_to_be_clickable(FBankLocators.SUBMIT_BUTTON))
        button.click()

    def get_alert_text_and_accept(self) -> str:
        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None

    def get_transfer_amount_value(self):
        amount_input = self.wait.until(EC.visibility_of_element_located(FBankLocators.SUM_INPUT))
        return amount_input.get_attribute("value")



