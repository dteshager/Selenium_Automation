import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException

from pathlib import Path
from dotenv import load_dotenv



debugging = True
load_dotenv()


LOGIN_PAGE=os.getenv('LOGIN_PAGE')
ACCOUNT_NUMBER=os.getenv('ACCOUNT_NUMBER')
LAST_NAME=os.getenv('LAST_NAME')
FIRST_NAME=os.getenv('FIRST_NAME')
PHONE_NUMBER=os.getenv('PHONE_NUMBER')
EMAIL_ADDRESS=os.getenv('USER_NAME')
PASSWORD=os.getenv('PASSWORD')
NAME=os.getenv('NAME')
EXP_DATE=os.getenv('EXP_DATE')
CVC=os.getenv('CVC')

script_directory = Path(__file__).resolve().parent
driver_path = script_directory.joinpath("chromedriver-win64", "chromedriver.exe")


chrome_options = Options()
if debugging:
    chrome_options.add_experimental_option("detach", True)

else:
    chrome_options.add_argument("--headless")

#to make the login info a password type
def set_field_to_password(driver, element_id):
    driver.execute_script(f"document.getElementById('{element_id}').type = 'password'")

#after we login to a page we need to wait some time to make sure everything is loaded.
def wait_for_element(driver, by, element_identifier, timeout=10):
    try:
        element_present = EC.element_to_be_clickable((by, element_identifier))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print(f"Timed out waiting for element {element_identifier}")
        return None
    return driver.find_element(by, element_identifier)



def login_to_account(driver):
    driver.get(LOGIN_PAGE)

    account_input = wait_for_element(driver, By.ID, "Login")
    password_input = wait_for_element(driver, By.ID, "Password")


    if account_input and password_input:
        set_field_to_password(driver, 'Login')
        set_field_to_password(driver, 'Password')
        account_input.send_keys(EMAIL_ADDRESS)
        password_input.send_keys(PASSWORD)

def buttons(driver):

    login_button = wait_for_element(driver, By.ID, "submit")
    if login_button:
        login_button.click()
#
    pay_now = wait_for_element(driver, By.XPATH,
                               '//a[contains(@class, "button") and contains(@class, "primary") and contains(@class, "positive")]')
    if pay_now:
        pay_now.click()


    next_button = wait_for_element(driver, By.ID, "subway-next")
    if next_button:
        next_button.click()



    iframe= wait_for_element(driver, By.ID, 'extPmtPageFrame')
    if iframe:
        driver.switch_to.frame(iframe)
        another_next = wait_for_element(driver, By.ID, "next")
        #
        credit = wait_for_element(driver, By.ID, "cc")
        if credit:
        #     credit.click()
                another_next.click()


        driver.switch_to.default_content()
#
#
#
def submit_payment(driver):

    new_iframe = wait_for_element(driver, By.ID, 'extPmtPageFrame')
    if new_iframe:
        driver.switch_to.frame(new_iframe)

        holder = wait_for_element(driver, By.ID, "CreditCard_name")
        number = wait_for_element(driver, By.ID, "CreditCard_cardNumber")
        expiration = wait_for_element(driver, By.ID, "CreditCard_expDate")
        cvc_num = wait_for_element(driver, By.ID, "CreditCard_cvc")
        pay_val = wait_for_element(driver, By.ID, "cardPay")

        if pay_val:
            pay_amt_str = pay_val.get_attribute("value")

            try:
                pay_amt_num = re.search(r'-?\d+\.?\d*', pay_amt_str)
                only_num = float(pay_amt_num.group(0))
                if only_num <= 0.00:
                    print('You have no due payment for now')
                    return False
                elif only_num >= 50:
                    print("Too much please look before you pay")
                    return False
            except ValueError:
                return False


        if (holder and number and expiration and cvc_num and pay_val):
            holder.send_keys(NAME)
            number.send_keys(ACCOUNT_NUMBER)
            expiration.send_keys(EXP_DATE)
            cvc_num.send_keys(CVC)

            pay_val.click()
        try:
            WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element(By.ID, "successMessage"))

            return True
        except TimeoutException:
            print('Payment failed')
            return False

def main():

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        login_to_account(driver)
        buttons(driver)
        submit_payment(driver)
    except WebDriverException as e:
        print(f"General WebDriver error: {e}")
    finally:
        if not debugging:
            driver.quit()
#
if __name__ == '__main__':
    main()