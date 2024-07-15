from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

def process_table(table_element, options, result):
    for option in options:
        currency_code = option.get_attribute("value").lower()
        result[currency_code] = []
        
        option.click()
        time.sleep(2)
        
        table_html = table_element.get_attribute("outerHTML")
        table_soup = BeautifulSoup(table_html, "html.parser")
        
        for row in table_soup.find_all("tr", class_="svelte-sdi4lo"):
            market_name_tag = row.find("a", class_="tab")
            if market_name_tag:
                market_name = market_name_tag.text.strip()
            else:
                market_name = ""
            
            address_tag = row.find("address")
            if address_tag:
                address = address_tag.text.strip()
            else:
                address = ""
            
            buy_rate_tag = row.find("span", title=f"{currency_code.upper()} - покупка")
            if buy_rate_tag:
                buy_rate = buy_rate_tag.text.strip()
            else:
                buy_rate = ""
            
            sell_rate_tag = row.find("span", title=f"{currency_code.upper()} - продажа")
            if sell_rate_tag:
                sell_rate = sell_rate_tag.text.strip()
            else:
                sell_rate = ""
            
            time_tag = row.find("time")
            if time_tag:
                time_str = time_tag["title"]
            else:
                time_str = ""
            
            result[currency_code].append({
                "market_name": market_name,
                "address": address,
                "buy_rate": buy_rate,
                "sell_rate": sell_rate,
                "time": time_str
            })

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

    with open(f'{city}.json', 'w', encoding='utf-8') as f:
        json.dump(result_in_city, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {city}.json")

    if city == "almaty":
        select_other = driver.find_element(By.XPATH, '//*[@id="kurs-table"]/main/table[2]/thead/tr/th[3]/span[2]/select')
        options_other = select_other.find_elements(By.TAG_NAME, "option")
        result_other = {}
        other_table = driver.find_element(By.XPATH, '//*[@id="kurs-table"]/main/table[2]')
        result_other = process_table(other_table, options_other, result_other)
        
        with open(f'{city}_table2.json', 'w', encoding='utf-8') as f:
            json.dump(result_other, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {city}_table2.json")