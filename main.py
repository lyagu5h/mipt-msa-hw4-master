from currency_converter import CurrencyConverter

CURRENCIES = [
    "CNY", 
    "EUR", 
    "GBP", 
    "RUB"
    ]

def main():
    amount = float(input("Введите значение в USD: \n"))
    converter = CurrencyConverter()

    for currency in CURRENCIES:
        try:
            result = converter.convert(amount, currency)
            print(f"{amount} USD to {currency}: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()