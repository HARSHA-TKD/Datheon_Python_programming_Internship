import csv
import os
from datetime import datetime

CSV_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "portfolio_history.csv"
)


def calculate_stock_value(quantity, buy_price, current_price):
    investment = quantity * buy_price
    market_value = quantity * current_price
    profit_loss = market_value - investment

    return investment, market_value, profit_loss


def display_portfolio(stocks):
    total_investment = 0
    total_value = 0

    print("\n========== STOCK PORTFOLIO ==========")

    for stock in stocks:
        name, quantity, buy_price, current_price = stock

        investment, value, profit_loss = calculate_stock_value(
            quantity, buy_price, current_price
        )

        total_investment += investment
        total_value += value

        print(f"\nStock: {name}")
        print(f"Quantity: {quantity}")
        print(f"Investment: Rs. {investment:.2f}")
        print(f"Current value: Rs. {value:.2f}")
        print(f"Profit/Loss: Rs. {profit_loss:.2f}")

    total_profit_loss = total_value - total_investment

    print("\n---------- TOTAL ----------")
    print(f"Total investment: Rs. {total_investment:.2f}")
    print(f"Current portfolio value: Rs. {total_value:.2f}")
    print(f"Total profit/loss: Rs. {total_profit_loss:.2f}")


def save_performance(total_investment, total_value, profit_loss):
    file_exists = os.path.exists(CSV_FILE)

    try:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Date", "Total Investment",
                    "Portfolio Value", "Profit Loss"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"{total_investment:.2f}",
                f"{total_value:.2f}",
                f"{profit_loss:.2f}"
            ])

        print("\nPortfolio performance saved to CSV.")

    except OSError:
        print("Error: Could not save portfolio history.")


def main():
    stocks = []

    print("Stock Portfolio Performance Tracker")
    print("Enter your stock details below.")
    print("Type 'done' when finished.")

    while True:
        name = input("\nStock name or symbol: ").strip()

        if name.lower() == "done":
            break

        if not name:
            print("Stock name cannot be empty.")
            continue

        try:
            quantity = int(input("Quantity owned: "))
            buy_price = float(input("Purchase price per share: Rs. "))
            current_price = float(input("Current price per share: Rs. "))

            if quantity <= 0 or buy_price < 0 or current_price < 0:
                print("Quantity must be positive and prices cannot be negative.")
                continue

        except ValueError:
            print("Please enter valid numbers.")
            continue

        stocks.append((name, quantity, buy_price, current_price))

    if not stocks:
        print("No stocks entered. Exiting.")
        return

    display_portfolio(stocks)

    total_investment = sum(
        quantity * buy_price
        for name, quantity, buy_price, current_price in stocks
    )

    total_value = sum(
        quantity * current_price
        for name, quantity, buy_price, current_price in stocks
    )

    save_performance(
        total_investment,
        total_value,
        total_value - total_investment
    )


if __name__ == "__main__":
    main()