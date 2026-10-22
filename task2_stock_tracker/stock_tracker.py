import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO_FILE = os.path.join(BASE_DIR, "portfolio.csv")
HISTORY_FILE = os.path.join(BASE_DIR, "portfolio_history.csv")


def load_portfolio():
    """Load saved stock holdings from CSV."""
    stocks = []

    if not os.path.exists(PORTFOLIO_FILE):
        return stocks

    try:
        with open(PORTFOLIO_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                stocks.append({
                    "symbol": row["symbol"],
                    "quantity": int(row["quantity"]),
                    "buy_price": float(row["buy_price"]),
                    "current_price": float(row["current_price"])
                })

    except (OSError, ValueError, KeyError):
        print("Warning: Could not load portfolio data.")

    return stocks


def save_portfolio(stocks):
    """Save holdings so they remain available after restarting."""
    try:
        with open(PORTFOLIO_FILE, "w", newline="", encoding="utf-8") as file:
            fields = ["symbol", "quantity", "buy_price", "current_price"]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(stocks)

    except OSError:
        print("Error: Could not save portfolio.")


def calculate_performance(stock):
    investment = stock["quantity"] * stock["buy_price"]
    market_value = stock["quantity"] * stock["current_price"]
    profit_loss = market_value - investment

    if investment > 0:
        return_percentage = (profit_loss / investment) * 100
    else:
        return_percentage = 0.0

    return {
        "investment": investment,
        "market_value": market_value,
        "profit_loss": profit_loss,
        "return_percentage": return_percentage
    }


def get_totals(stocks):
    investment = 0.0
    market_value = 0.0

    for stock in stocks:
        result = calculate_performance(stock)
        investment += result["investment"]
        market_value += result["market_value"]

    profit_loss = market_value - investment
    return investment, market_value, profit_loss


def add_stock(stocks):
    symbol = input("Stock name or symbol: ").strip().upper()

    if not symbol:
        print("Symbol cannot be empty.")
        return

    try:
        quantity = int(input("Quantity owned: "))
        buy_price = float(input("Average purchase price (Rs.): "))
        current_price = float(input("Current price (Rs.): "))

        if quantity <= 0 or buy_price < 0 or current_price < 0:
            print("Quantity must be positive; prices cannot be negative.")
            return

    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    # Update an existing holding if the symbol already exists.
    for stock in stocks:
        if stock["symbol"] == symbol:
            stock["quantity"] += quantity

            old_cost = (stock["quantity"] - quantity) * stock["buy_price"]
            new_cost = quantity * buy_price
            stock["buy_price"] = (
                (old_cost + new_cost) / stock["quantity"]
            )
            stock["current_price"] = current_price

            save_portfolio(stocks)
            print(f"{symbol} holding updated successfully.")
            return

    stocks.append({
        "symbol": symbol,
        "quantity": quantity,
        "buy_price": buy_price,
        "current_price": current_price
    })

    save_portfolio(stocks)
    print(f"{symbol} added successfully.")


def show_dashboard(stocks):
    if not stocks:
        print("Your portfolio is empty. Add a stock first.")
        return

    investment, market_value, profit_loss = get_totals(stocks)
    return_percentage = (
        profit_loss / investment * 100 if investment else 0.0
    )

    print("\n" + "=" * 65)
    print("              PORTFOLIO PERFORMANCE DASHBOARD")
    print("=" * 65)

    print(f"{'SYMBOL':<12}{'QTY':>6}{'INVESTED':>14}"
          f"{'VALUE':>14}{'P/L':>14}")

    for stock in stocks:
        result = calculate_performance(stock)
        print(
            f"{stock['symbol']:<12}"
            f"{stock['quantity']:>6}"
            f"{result['investment']:>14.2f}"
            f"{result['market_value']:>14.2f}"
            f"{result['profit_loss']:>14.2f}"
        )

    print("-" * 65)
    print(f"Total investment : Rs. {investment:,.2f}")
    print(f"Current value    : Rs. {market_value:,.2f}")
    print(f"Profit / Loss    : Rs. {profit_loss:,.2f}")
    print(f"Overall return   : {return_percentage:.2f}%")

    if profit_loss > 0:
        print("Performance      : PORTFOLIO IN PROFIT")
    elif profit_loss < 0:
        print("Performance      : PORTFOLIO IN LOSS")
    else:
        print("Performance      : BREAK-EVEN")

    print("=" * 65)


def analyze_performers(stocks):
    if not stocks:
        print("Add stocks to analyze performance.")
        return

    ranked = sorted(
        stocks,
        key=lambda stock: calculate_performance(stock)["return_percentage"],
        reverse=True
    )

    print("\nPERFORMANCE RANKING")
    print("-" * 45)

    for rank, stock in enumerate(ranked, start=1):
        result = calculate_performance(stock)
        print(
            f"{rank}. {stock['symbol']:<12}"
            f"{result['return_percentage']:>8.2f}% return"
            f"  P/L: Rs. {result['profit_loss']:,.2f}"
        )

    print("\nBest performer :", ranked[0]["symbol"])
    print("Weakest performer:", ranked[-1]["symbol"])
    print("Note: Past returns do not predict future returns.")


def show_allocation(stocks):
    if not stocks:
        print("Your portfolio is empty.")
        return

    _, market_value, _ = get_totals(stocks)

    print("\nPORTFOLIO ALLOCATION")
    print("-" * 45)

    for stock in sorted(
        stocks,
        key=lambda item: item["quantity"] * item["current_price"],
        reverse=True
    ):
        value = stock["quantity"] * stock["current_price"]
        percentage = value / market_value * 100 if market_value else 0

        bar = "#" * int(percentage / 5)

        print(
            f"{stock['symbol']:<12} {percentage:6.2f}% "
            f"Rs. {value:,.2f} {bar}"
        )

    if stocks:
        largest = max(
            stocks,
            key=lambda item: item["quantity"] * item["current_price"]
        )
        largest_value = largest["quantity"] * largest["current_price"]
        concentration = (
            largest_value / market_value * 100 if market_value else 0
        )

        print(f"\nLargest holding: {largest['symbol']}")

        if concentration >= 50:
            print("Notice: Over half of the portfolio value is in one holding.")


def save_snapshot(stocks):
    if not stocks:
        print("Add stocks before saving a snapshot.")
        return

    investment, market_value, profit_loss = get_totals(stocks)
    percentage = profit_loss / investment * 100 if investment else 0

    file_exists = os.path.exists(HISTORY_FILE)

    try:
        with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists or os.path.getsize(HISTORY_FILE) == 0:
                writer.writerow([
                    "timestamp", "investment", "market_value",
                    "profit_loss", "return_percentage"
                ])

            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                f"{investment:.2f}",
                f"{market_value:.2f}",
                f"{profit_loss:.2f}",
                f"{percentage:.2f}"
            ])

        print("Performance snapshot saved successfully.")

    except OSError:
        print("Error: Could not save performance history.")


def view_history():
    if not os.path.exists(HISTORY_FILE):
        print("No history yet. Save a snapshot first.")
        return

    try:
        with open(HISTORY_FILE, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        if not rows:
            print("No performance snapshots found.")
            return

        print("\nSAVED PERFORMANCE HISTORY")
        print("-" * 75)

        for row in rows:
            print(
                f"{row['timestamp']} | "
                f"Value: Rs. {float(row['market_value']):,.2f} | "
                f"P/L: Rs. {float(row['profit_loss']):,.2f} | "
                f"Return: {float(row['return_percentage']):.2f}%"
            )

        if len(rows) >= 2:
            first = float(rows[0]["market_value"])
            latest = float(rows[-1]["market_value"])
            change = latest - first

            print("\nChange since first saved snapshot:")
            print(f"Rs. {change:,.2f}")

            if first:
                print(f"Value change: {change / first * 100:.2f}%")

        print(
            "\nReminder: This comparison uses saved snapshots and "
            "does not account for deposits, withdrawals, or trades "
            "between snapshots."
        )

    except (OSError, ValueError, KeyError):
        print("Error: Could not read history. Check the CSV file.")


def main():
    stocks = load_portfolio()

    while True:
        print("\n" + "=" * 45)
        print("       STOCK PORTFOLIO ANALYZER")
        print("=" * 45)
        print("1. Add or update stock")
        print("2. View performance dashboard")
        print("3. Analyze best and worst performers")
        print("4. View portfolio allocation")
        print("5. Save performance snapshot")
        print("6. View historical performance")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_stock(stocks)
        elif choice == "2":
            show_dashboard(stocks)
        elif choice == "3":
            analyze_performers(stocks)
        elif choice == "4":
            show_allocation(stocks)
        elif choice == "5":
            save_snapshot(stocks)
        elif choice == "6":
            view_history()
        elif choice == "7":
            save_portfolio(stocks)
            print("Portfolio saved. Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()