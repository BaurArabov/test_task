import json
import os

def get_rates(data, rate_type):
    rates = []
    for entry in data:
        try:
            rate = float(entry[rate_type])
            if rate > 0:
                rates.append((rate, entry))
        except ValueError:
            continue
    return rates

def find_max_min(data):
    result = {}
    for currency, entries in data.items():
        buy_rates = get_rates(entries, "buy_rate")
        sell_rates = get_rates(entries, "sell_rate")

        if buy_rates:
            max_buy_rate = max(buy_rates, key=lambda x: x[0])[1]
            min_buy_rate = min(buy_rates, key=lambda x: x[0])[1]
        else:
            max_buy_rate = min_buy_rate = {
                "market_name": "",
                "address": "",
                "buy_rate": "0",
                "sell_rate": "0"
            }

        if sell_rates:
            max_sell_rate = max(sell_rates, key=lambda x: x[0])[1]
            min_sell_rate = min(sell_rates, key=lambda x: x[0])[1]
        else:
            max_sell_rate = min_sell_rate = {
                "market_name": "",
                "address": "",
                "buy_rate": "0",
                "sell_rate": "0"
            }

        result[currency] = {
            f"{currency}-max-buy-rate": max_buy_rate,
            f"{currency}-min-buy-rate": min_buy_rate,
            f"{currency}-max-sell-rate": max_sell_rate,
            f"{currency}-min-sell-rate": min_sell_rate,
        }

    return result


output_folder = 'max_min_cities'
os.makedirs(output_folder, exist_ok=True)

for file_name in os.listdir('jsons/'):
    if file_name.endswith('.json'):
        city_name = file_name.rsplit('.', 1)[0]
        file_path = os.path.join('jsons/', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            result = find_max_min(data)
            output_file = os.path.join(output_folder, f'{city_name}.json')
            with open(output_file, 'w', encoding='utf-8') as f_out:
                json.dump(result, f_out, ensure_ascii=False, indent=4)
            print(f"Results for {city_name} have been written to {output_file}")