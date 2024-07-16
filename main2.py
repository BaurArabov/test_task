from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def extract_table_data(row, currency_code):
    market_name_tag = row.find("a", class_="tab")
    market_name = market_name_tag.text.strip() if market_name_tag else ""
    
    address_tag = row.find("address")
    address = address_tag.text.strip() if address_tag else ""
    
    buy_rate_tag = row.find("span", title=f"{currency_code.upper()} - покупка")
    buy_rate = buy_rate_tag.text.strip() if buy_rate_tag else ""
    
    sell_rate_tag = row.find("span", title=f"{currency_code.upper()} - продажа")
    sell_rate = sell_rate_tag.text.strip() if sell_rate_tag else ""
    
    time_tag = row.find("time")
    time_str = time_tag["title"] if time_tag else ""
    
    return {
        "market_name": market_name,
        "address": address,
        "buy_rate": buy_rate,
        "sell_rate": sell_rate,
        "time": time_str
    }

def process_table(table_element, options, result):
    for option in options:
        currency_code = option.get_attribute("value").lower()
        result[currency_code] = {"max-buy": {}, "min-buy": {}, "max-sell": {}, "min-sell": {}}

        option.click()
        time.sleep(1)

        buy_rate_button = table_element.find_element(By.XPATH, './/span[@data-tooltip="Выгодная покупка"]')
        sell_rate_button = table_element.find_element(By.XPATH, './/span[@data-tooltip="Выгодная продажа"]')

        buy_rate_button.click()
        time.sleep(1)

        table_html = table_element.get_attribute("outerHTML")
        table_soup = BeautifulSoup(table_html, "html.parser")
        first_row = table_soup.find("tr", class_="svelte-sdi4lo")
        result[currency_code]["max-buy"] = extract_table_data(first_row, currency_code)

        buy_rate_button.click()
        time.sleep(1)

        table_html = table_element.get_attribute("outerHTML")
        table_soup = BeautifulSoup(table_html, "html.parser")
        first_row = table_soup.find("tr", class_="svelte-sdi4lo")
        result[currency_code]["min-buy"] = extract_table_data(first_row, currency_code)

        sell_rate_button.click()
        time.sleep(1)

        table_html = table_element.get_attribute("outerHTML")
        table_soup = BeautifulSoup(table_html, "html.parser")
        first_row = table_soup.find("tr", class_="svelte-sdi4lo")
        result[currency_code]["min-sell"] = extract_table_data(first_row, currency_code)

        sell_rate_button.click()
        time.sleep(1)

        table_html = table_element.get_attribute("outerHTML")
        table_soup = BeautifulSoup(table_html, "html.parser")
        first_row = table_soup.find("tr", class_="svelte-sdi4lo")
        result[currency_code]["max-sell"] = extract_table_data(first_row, currency_code)

    return result

driver = webdriver.Chrome()

cities = [
    "almaty",
    "astana",
    "aksu (pavlodar region)",
    "aktau",
    "aktobe",
    "kaskelen",
    "kostanai",
    "pavlodar",
    "ridder",
    "semei",
    "taldykorgan",
    "uralsk",
    "shymkent",
    "ekibastuz"
]

for city in cities:
    driver.get(f"https://kurs.kz/site/index?city={city}")
    select_in_city = driver.find_element(By.XPATH, '//*[@id="kurs-table"]/main/table[1]/thead/tr/th[3]/span[2]/select')

    options_in_city = select_in_city.find_elements(By.TAG_NAME, "option")
    result_in_city = {}
    in_city_table = driver.find_element(By.XPATH, '//*[@id="kurs-table"]/main/table[1]')
    result_in_city = process_table(in_city_table, options_in_city, result_in_city)

    with open(f'json_files/{city}.json', 'w', encoding='utf-8') as f:
        json.dump(result_in_city, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {city}.json")