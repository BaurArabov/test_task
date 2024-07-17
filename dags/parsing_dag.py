from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

def parse_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    user_agent = 'userMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('-headless')

    remote_webdriver = 'remote_chromedriver'

    with webdriver.Remote(f'{remote_webdriver}:4444/wd/hub', options=options) as driver:

        driver.get(f"https://kurs.kz")
        driver.implicitly_wait(10)
        driver.maximize_window()
        

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

            print(f"Result for {city}: {result_in_city}")


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 7, 16),
}

with DAG('parse_data_dag', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    parse_data_task = PythonOperator(
        task_id='parse_data',
        python_callable=parse_data,
    )