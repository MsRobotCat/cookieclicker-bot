from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException

import time
URL = "https://orteil.dashnet.org/cookieclicker/"


def get_score():
    score_text = driver.find_element(By.XPATH, '//*[@id="cookies"]')
    try:
        score = score_text.text.splitlines()[0].split()[0]
    except StaleElementReferenceException:
        score = score_text.text.splitlines()[0].split()[0]
    score = score.replace(',', '')
    score_int = int(score)
    return score_int


def get_price_list():
    prices = driver.find_elements(By.CLASS_NAME, 'price')
    price_list = []
    for i in range(len(prices)):
        try:
            price = driver.find_elements(By.CLASS_NAME, 'price')[i]  # Move this inside the loop
            price_list.append(price.text)
        except StaleElementReferenceException:
            time.sleep(0.5)
            price = driver.find_elements(By.CLASS_NAME, 'price')[i]  # Try to find the element again if it was stale
            price_list.append(price.text)
    int_price_list = []
    for price in price_list:
        try:
            price = int(price)
            int_price_list.append(price)
        except ValueError:
            price = 0
            int_price_list.append(price)
    return int_price_list



def click_cookie():
    try:
        cookie = driver.find_element(By.ID, 'bigCookie')
        cookie.click()
    except StaleElementReferenceException:
        cookie = driver.find_element(By.ID, 'bigCookie')
        cookie.click()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

wait = WebDriverWait(driver, 10)

consent = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fc-button-label')))
consent.click()
language = wait.until(EC.presence_of_element_located((By.ID, 'langSelect-EN')))
language.click()


timeout2 = time.time() + 2*60
while time.time() < timeout2:
    timeout1 = time.time() + 45
    while time.time() < timeout1:
        click_cookie()
    for i in range(len(get_price_list()) - 1, -1, -1): # reverse the list so we can prioritise the most expensive items
        if get_score() >= get_price_list()[i]:
            try:
                upgrade = driver.find_element(By.XPATH, f'//*[@id="product{i}"]')
                upgrade.click()
            except StaleElementReferenceException:
                upgrade = driver.find_element(By.XPATH, f'//*[@id="product{i}"]')
                upgrade.click()
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException:
                pass
            except NoSuchElementException:
                pass
            except IndexError:
                pass
cookies_per_sec = driver.find_element(By.ID, 'cookiesPerSecond').text.split()[2]
print(f"Cookies per second: {cookies_per_sec}")

