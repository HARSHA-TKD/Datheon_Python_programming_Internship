# 📊 Stock Portfolio Performance Analyzer

**A Python-based portfolio tracking and performance analysis application.**

Stock Portfolio Performance Analyzer is a command-line application developed using Python to help users monitor stock holdings, evaluate investment performance, and maintain historical portfolio records.

The application calculates portfolio valuation, profit and loss, percentage returns, individual stock performance, and portfolio allocation. It also stores holdings and performance snapshots using CSV files for persistent data management.

---

## 🚀 Key Features

### 1. Portfolio Management
- Add new stock holdings.
- Update existing stock information.
- Store stock symbols, quantities, purchase prices, and current prices.
- Maintain holdings between application sessions.

### 2. Performance Analytics
- Calculate total invested capital.
- Calculate current portfolio market value.
- Determine absolute profit or loss.
- Calculate portfolio return percentage.
- Analyze individual stock performance.

### 3. Stock Performance Ranking
- Rank holdings based on percentage returns.
- Identify the best-performing stock.
- Identify the lowest-performing stock.
- Compare individual holding performance.

### 4. Portfolio Allocation Analysis
- Calculate the percentage allocation of each holding.
- Display a simple text-based allocation chart.
- Identify concentration in a single holding.

### 5. Historical Performance Tracking
- Save timestamped portfolio snapshots.
- Store investment value, market value, profit/loss, and returns.
- Review previously saved performance records.

### 6. Data Persistence
- Store portfolio holdings in CSV format.
- Maintain historical records in a separate CSV file.
- Automatically create data files when required.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core application |
| CSV | Portfolio and history storage |
| Datetime | Timestamp generation |
| OS | File and directory handling |
| Unittest | Automated testing |

**Dependencies:** Python standard library only. No external packages required.

---

## 📂 Project Structure

```text
task2_stock_tracker/
│
├── stock_tracker.py
│   └── Main application
│
├── test_stock_tracker.py
│   └── Automated unit tests
│
├── README.md
│   └── Project documentation
│
├── holdings.csv
│   └── Saved stock holdings (generated)
│
└── portfolio_history.csv
    └── Historical snapshots (generated)
```

---

## ⚙️ Installation & Execution

### Prerequisites

- Python 3.8 or later
- Visual Studio Code or any Python-compatible editor

### Step 1 — Clone the repository

```bash
git clone https://github.com/HARSHA-TKD/Datheon_Python_Programming_Internship.git
```

### Step 2 — Navigate to the project

```bash
cd Datheon_Python_Programming_Internship/task2_stock_tracker
```

### Step 3 — Run the application

```bash
python stock_tracker.py
```

---

## 🖥️ Application Menu

```text
==========================================
      STOCK PORTFOLIO ANALYZER
==========================================
1. Add or update a stock
2. View performance dashboard
3. Rank best and worst performers
4. View portfolio allocation
5. Save performance snapshot
6. View historical performance
7. Exit
```

---

## 📈 Performance Calculation Methodology

The application uses the following financial calculations.

**Total Investment**

```text
Quantity × Purchase Price
```

**Current Market Value**

```text
Quantity × Current Price
```

**Profit / Loss**

```text
Current Market Value - Total Investment
```

**Return Percentage**

```text
(Profit / Loss ÷ Total Investment) × 100
```

**Portfolio Allocation**

```text
(Individual Stock Value ÷ Total Portfolio Value) × 100
```

These calculations provide a basic view of portfolio performance before considering brokerage fees, taxes, dividends, and other costs.

---

## 🧪 Testing & Validation

The project includes automated tests using Python's built-in `unittest` framework.

### Run the tests

```bash
python -m unittest -v test_stock_tracker.py
```

### Test coverage

- Profit calculation
- Loss calculation
- Zero profit/loss calculation
- Zero current-price handling
- Portfolio total calculations
- Empty portfolio handling

---

## 📊 Data Management

The application maintains two separate CSV files.

**holdings.csv**

Stores the latest stock holdings and their manually entered prices.

**portfolio_history.csv**

Stores timestamped performance snapshots for historical comparison.

Snapshots are recorded when the user selects the save-performance option.

---

## ⚠️ Current Limitations

- Stock prices are entered manually.
- Live market data integration is not currently implemented.
- Historical tracking depends on user-created snapshots.
- Calculations do not account for brokerage charges, taxes, or dividends.
- This application is intended for educational portfolio analysis, not financial advice.

---

## 🔮 Future Enhancements

Potential improvements include:

- Integration with a market-data API.
- Interactive portfolio performance charts.
- Advanced historical return analysis.
- Sector-wise portfolio allocation.
- Exportable portfolio performance reports.
- More advanced risk and volatility metrics.

---

## 👨‍💻 Developer

**Harsha Vardhan V G**

Datheon Python Programming Internship

**Project:** Task 2 – Stock Portfolio Performance Analyzer

---

*Developed as part of the Datheon Python Programming Internship to strengthen Python programming, data handling, financial calculations, and software testing skills.*