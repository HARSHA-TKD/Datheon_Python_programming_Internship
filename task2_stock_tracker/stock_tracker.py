
import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOLDINGS_FILE = os.path.join(BASE_DIR, "holdings.csv")
HISTORY_FILE = os.path.join(BASE_DIR, "portfolio_history.csv")


def load_holdings():
    """Load saved stock holdings."""
    stocks = {}

    if not os.path.exists(HOLDINGS_FILE):
        return stocks

    try:
        with open(HOLDINGS_FILE, "r", newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                symbol = row["symbol"]
                stocks[symbol] = {
                    "quantity": int(row["quantity"]),
                    "buy_price": float(row["buy_price"]),
                    "current_price": float(row["current_price"])
                }
    except (OSError, ValueError, KeyError):
        print("Could not read holdings.csv. Check its contents.")
        return {}

    return stocks


def save_holdings(stocks):
    """Save holdings so they remain available next time."""
    try:
        with open(HOLDINGS_FILE, "w", newline="", encoding="utf-8") as file:
            fields = ["symbol", "quantity", "buy_price", "current_price"]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for symbol, data in stocks.items():
                writer.writerow({
                    "symbol": symbol,
                    "quantity": data["quantity"],
                    "buy_price": data["buy_price"],
                    "current_price": data["current_price"]
                })
        return True
    except OSError:
        print("Could not save holdings.")
        return False


def analyze_stock(symbol, data):
    quantity = data["quantity"]
    buy_price = data["buy_price"]
    current_price = data["current_price"]

    investment = quantity * buy_price
    market_value = quantity * current_price
    profit_loss = market_value - investment

    if investment > 0:
        return_percent = (profit_loss / investment) * 100
    else:
        return_percent = 0.0

    return {
        "symbol": symbol,
        "quantity": quantity,
        "investment": investment,
        "market_value": market_value,
        "profit_loss": profit_loss,
        "return_percent": return_percent
    }


def get_report(stocks):
    report = [analyze_stock(symbol, data)
              for symbol, data in stocks.items()]

    total_investment = sum(item["investment"] for item in report)
    total_value = sum(item["market_value"] for item in report)
    total_profit_loss = total_value - total_investment

    if total_investment > 0:
        total_return = total_profit_loss / total_investment * 100
    else:
        total_return = 0.0

    return report, total_investment, total_value, total_profit_loss, total_return


def show_dashboard(stocks):
    if not stocks:
        print("\nYour portfolio is empty. Add a holding first.")
        return

    report, investment, value, profit_loss, return_percent = get_report(stocks)

    print("\n" + "=" * 58)
    print("             PORTFOLIO PERFORMANCE DASHBOARD")
    print("=" * 58)
    print(f"Total investment : Rs. {investment:,.2f}")
    print(f"Current value   : Rs. {value:,.2f}")
    print(f"Profit / Loss   : Rs. {profit_loss:+,.2f}")
    print(f"Return          : {return_percent:+.2f}%")
    print("-" * 58)
    print(f"{'SYMBOL':<12}{'INVESTED':>13}{'VALUE':>13}{'P/L':>13}")
    print("-" * 58)

    for item in report:
        print(
            f"{item['symbol']:<12}"
            f"{item['investment']:>13,.2f}"
            f"{item['market_value']:>13,.2f}"
            f"{item['profit_loss']:>+13,.2f}"
        )

    print("=" * 58)


def show_performance_ranking(stocks):
    if not stocks:
        print("\nNo holdings to analyze.")
        return

    report, *_ = get_report(stocks)
    ranked = sorted(
        report,
        key=lambda item: item["return_percent"],
        reverse=True
    )

    print("\nPERFORMANCE RANKING")
    print("-" * 48)

    for rank, item in enumerate(ranked, start=1):
        print(
            f"{rank}. {item['symbol']:<12} "
            f"{item['return_percent']:+.2f}% "
            f"(P/L: Rs. {item['profit_loss']:+,.2f})"
        )

    print("\nBest performer :", ranked[0]["symbol"])
    print("Lowest performer:", ranked[-1]["symbol"])


def show_allocation(stocks):
    if not stocks:
        print("\nNo holdings to analyze.")
        return

    report, _, total_value, _, _ = get_report(stocks)

    print("\nPORTFOLIO ALLOCATION")
    print("-" * 42)

    for item in sorted(
        report, key=lambda item: item["market_value"], reverse=True
    ):
        if total_value > 0:
            allocation = item["market_value"] / total_value * 100
        else:
            allocation = 0.0

        bar = "#" * int(allocation / 5)
        print(f"{item['symbol']:<12} {allocation:6.2f}% {bar}")

    if total_value > 0:
        largest = max(report, key=lambda item: item["market_value"])
        share = largest["market_value"] / total_value * 100

        if share >= 50:
            print(
                f"\nConcentration notice: {largest['symbol']} represents "
                f"{share:.1f}% of portfolio value."
            )


def save_snapshot(stocks):
    if not stocks:
        print("\nNo holdings available to save.")
        return

    _, investment, value, profit_loss, return_percent = get_report(stocks)
    file_exists = os.path.exists(HISTORY_FILE)

    try:
        with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:
            fields = [
                "timestamp", "investment", "market_value",
                "profit_loss", "return_percent"
            ]
            writer = csv.DictWriter(file, fieldnames=fields)

            if not file_exists or os.path.getsize(HISTORY_FILE) == 0:
                writer.writeheader()

            writer.writerow({
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "investment": f"{investment:.2f}",
                "market_value": f"{value:.2f}",
                "profit_loss": f"{profit_loss:.2f}",
                "return_percent": f"{return_percent:.2f}"
            })

        print("Performance snapshot saved.")
    except OSError:
        print("Could not save the performance snapshot.")


def show_history():
    if not os.path.exists(HISTORY_FILE):
        print("\nNo performance history yet. Save a snapshot first.")
        return

    print("\nSAVED PERFORMANCE HISTORY")
    print("-" * 72)

    try:
        with open(HISTORY_FILE, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        if not rows:
            print("No snapshots recorded yet.")
            return

        for row in rows:
            print(
                f"{row['timestamp']} | "
                f"Value: Rs. {float(row['market_value']):,.2f} | "
                f"P/L: Rs. {float(row['profit_loss']):+,.2f} | "
                f"Return: {float(row['return_percent']):+.2f}%"
            )
    except (OSError, ValueError, KeyError):
        print("Could not read the performance history.")


def add_or_update_stock(stocks):
    symbol = input("Stock symbol/name: ").strip().upper()

    if not symbol:
        print("Symbol cannot be empty.")
        return

    try:
        quantity = int(input("Total quantity owned: "))
        buy_price = float(input("Average purchase price per share: Rs. "))
        current_price = float(input("Current price per share: Rs. "))

        if quantity <= 0 or buy_price <= 0 or current_price < 0:
            print("Quantity and purchase price must be positive; current price cannot be negative.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    stocks[symbol] = {
        "quantity": quantity,
        "buy_price": buy_price,
        "current_price": current_price
    }

    if save_holdings(stocks):
        print(f"{symbol} saved successfully.")


def main():
    stocks = load_holdings()

    while True:
        print("\n" + "=" * 42)
        print("      STOCK PORTFOLIO ANALYZER")
        print("=" * 42)
        print("1. Add or update a stock")
        print("2. View performance dashboard")
        print("3. Rank best and worst performers")
        print("4. View portfolio allocation")
        print("5. Save performance snapshot")
        print("6. View historical performance")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_or_update_stock(stocks)
        elif choice == "2":
            show_dashboard(stocks)
        elif choice == "3":
            show_performance_ranking(stocks)
        elif choice == "4":
            show_allocation(stocks)
        elif choice == "5":
            save_snapshot(stocks)
        elif choice == "6":
            show_history()
        elif choice == "7":
            print("Thanks for using Stock Portfolio Analyzer!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
