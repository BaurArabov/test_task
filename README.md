## Чтобы клонировать репозиторий на ваш локальный компьютер, выполните команду:

```bash
git clone https://github.com/BaurArabov/test_task.git

cd test_task.git

docker-compose run -d
```

## Запуск приложения

После клонирования, запустите приложение с помощью Docker:

```bash
docker-compose up
```

Перейдите на localhost:8080 и войдите в систему:

- Username: _airflow_
- Password: _airflow_

# Запуск DAG

1. Найдите DAG с именем parse_data_dag.
2. Активируйте и запустите его.

Это запустит скрипт для парсинга и сбора данных о валютных курсах для каждого рынка города, показывая максимальные и минимальные курсы покупки и продажи.

<<<<<<< HEAD

## Пример вывода

Результат для Алматы:

```json
{
  "usd": {
    "max-buy": {
      "market_name": "DIMAK EXCHANGE",
      "address": "6-й мкр., 5, (по пр. Абая не доезжая ул. Саина, по верхней стороне)",
      "buy_rate": "475.2",
      "sell_rate": "476.2",
      "time": "17.07.2024, 15:35:49"
    },
    "min-buy": {
      "market_name": "Bereke Exchange",
      "address": "ул. Желтоксан, 159 (уг.ул. Курмангазы, 70)",
      "buy_rate": "474.3",
      "sell_rate": "476",
      "time": "17.07.2024, 12:46:26"
    },
    "max-sell": {
      "market_name": "TEMA",
      "address": "пр. Абылай хана, 33, уг.пр.Райымбека (цокольный этаж)",
      "buy_rate": "475",
      "sell_rate": "478",
      "time": "17.07.2024, 11:13:34"
    },
    "min-sell": {
      "market_name": "Большая  Монета",
      "address": "пр. Сейфуллина 565, уг. ул. Кабанбай батыра",
      "buy_rate": "474.8",
      "sell_rate": "475.8",
      "time": "17.07.2024, 13:33:02"
    }
  },
  "eur": {
    "max-buy": {
      "market_name": "DOSTYK Exchange",
      "address": "ул. Сатпаева, 2 (уг. пр. Достык, рядом с кафе \"Breakfast\")",
      "buy_rate": "518.5",
      "sell_rate": "521.5",
      "time": "17.07.2024, 18:01:40"
    },
    "min-buy": {
      "market_name": "TEMA",
      "address": "пр. Абылай хана, 33, уг.пр.Райымбека (цокольный этаж)",
      "buy_rate": "512",
      "sell_rate": "522",
      "time": "17.07.2024, 11:13:34"
    },
    "max-sell": {
      "market_name": "TEMA",
      "address": "пр. Абылай хана, 33, уг.пр.Райымбека (цокольный этаж)",
      "buy_rate": "512",
      "sell_rate": "522",
      "time": "17.07.2024, 11:13:34"
    },
    "min-sell": {
      "market_name": "Лидер Эксчейндж",
      "address": "мкр. Айнабулак, 9а",
      "buy_rate": "517",
      "sell_rate": "520",
      "time": "17.07.2024, 14:48:51"
    }
  }
}
```
