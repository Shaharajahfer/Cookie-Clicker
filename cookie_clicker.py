from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "C:\\Users\\Shaharabanu's\\Application\\chromedriver.exe"
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

timeout = time.time() + 5   # 5 Sec
five_min = time.time() + 60*5   # 5Min
driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element(by=By.ID, value="cookie")
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
items_id = [item.get_attribute("id") for item in items]

while True:
    cookie.click()
    if time.time() > timeout:

        #Get number of cookies
        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        no_of_cookies = int(money_element)
        print(f"No of cookies: {no_of_cookies}")

        # Get all upgrade <b> tags
        all_prices = [ele.text for ele in driver.find_elements(by=By.CSS_SELECTOR, value="#store b")]
        affordable_upgrades = []
        prices = []
        for ele in all_prices:
            if ele == all_prices[-1]:
                break
            price = int(ele.split("-")[1].strip().replace(",", ""))
            prices.append(price)

            if price < no_of_cookies:
                affordable_upgrades.append(price)

        # Create dictionary of store items and prices
        cookie_upgrades = {prices[n]: items_id[n] for n in range(len(prices))}
        print(f"Upgrades: {cookie_upgrades}")

        if len(affordable_upgrades) != 0:
            expensive_upgrade = max(affordable_upgrades)
            print(f"expensive upgrade: {expensive_upgrade}")
            driver.find_element(by=By.ID, value=cookie_upgrades[expensive_upgrade]).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookies_per_sec = driver.find_element(by=By.ID, value="cps").text
        print(cookies_per_sec)
        break

driver.quit()
