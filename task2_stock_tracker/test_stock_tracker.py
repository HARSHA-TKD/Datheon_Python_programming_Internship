
import unittest
import stock_tracker


class TestStockPortfolio(unittest.TestCase):

    def test_profit_calculation(self):
        result = stock_tracker.analyze_stock(
            "DEMO", {
                "quantity": 10,
                "buy_price": 100,
                "current_price": 120
            }
        )

        self.assertEqual(result["investment"], 1000)
        self.assertEqual(result["market_value"], 1200)
        self.assertEqual(result["profit_loss"], 200)
        self.assertAlmostEqual(result["return_percent"], 20.0)

    def test_loss_calculation(self):
        result = stock_tracker.analyze_stock(
            "DEMO", {
                "quantity": 10,
                "buy_price": 100,
                "current_price": 80
            }
        )

        self.assertEqual(result["profit_loss"], -200)
        self.assertAlmostEqual(result["return_percent"], -20.0)

    def test_no_profit_or_loss(self):
        result = stock_tracker.analyze_stock(
            "DEMO", {
                "quantity": 5,
                "buy_price": 100,
                "current_price": 100
            }
        )

        self.assertEqual(result["profit_loss"], 0)
        self.assertEqual(result["return_percent"], 0)

    def test_zero_current_price(self):
        result = stock_tracker.analyze_stock(
            "DEMO", {
                "quantity": 5,
                "buy_price": 100,
                "current_price": 0
            }
        )

        self.assertEqual(result["market_value"], 0)
        self.assertEqual(result["profit_loss"], -500)
        self.assertEqual(result["return_percent"], -100)

    def test_portfolio_totals(self):
        stocks = {
            "DEMO1": {
                "quantity": 10,
                "buy_price": 100,
                "current_price": 120
            },
            "DEMO2": {
                "quantity": 5,
                "buy_price": 200,
                "current_price": 180
            }
        }

        report, investment, value, profit_loss, return_percent = (
            stock_tracker.get_report(stocks)
        )

        self.assertEqual(len(report), 2)
        self.assertEqual(investment, 2000)
        self.assertEqual(value, 2100)
        self.assertEqual(profit_loss, 100)
        self.assertAlmostEqual(return_percent, 5.0)

    def test_empty_portfolio(self):
        report, investment, value, profit_loss, return_percent = (
            stock_tracker.get_report({})
        )

        self.assertEqual(report, [])
        self.assertEqual(investment, 0)
        self.assertEqual(value, 0)
        self.assertEqual(profit_loss, 0)
        self.assertEqual(return_percent, 0)


if __name__ == "__main__":
    unittest.main()
