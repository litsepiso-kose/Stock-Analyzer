# Stock Performance Analyzer 

This project is a **Stock Performance Analyzer** that uses the `yfinance` library to fetch historical stock data and visualize key financial indicators over time. The main purpose of this tool is to analyze the stock's annualized returns, moving averages, and Relative Strength Index (RSI) to provide insights into its performance.

## Features:

* **Data Fetching:**
  Retrieves historical stock data from Yahoo Finance for analysis.

* **Annualized Return Calculation:**
  Computes annualized returns for:

  * 1-Year
  * 3-Year
  * Since IPO

* **Technical Indicators:**

  * **Moving Averages:**

    * 14-day Moving Average (MA14)
    * 20-day Moving Average (MA20)
  * **Relative Strength Index (RSI):**

    * Identifies overbought (RSI > 70) and oversold (RSI < 30) conditions.

* **Data Visualization:**

  * Interactive line charts using `Plotly` to visualize:

    * Closing prices with MA14 & MA20
    * RSI with indicators for overbought and oversold levels

* **Error Handling:**
  Handles cases with insufficient data gracefully and logs meaningful error messages.

## Libraries Used:

* **yfinance:** To fetch historical stock data
* **pandas:** For data manipulation
* **plotly:** For interactive data visualization
* **datetime:** To manage date ranges
* **time:** To handle request throttling

## Usage:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/stock-performance-analyzer.git
   cd stock-performance-analyzer
   ```

2. Install dependencies:

   ```bash
   pip install yfinance pandas plotly
   ```

3. Run the script:

   ```bash
   python stock_analyzer.py
   ```

4. Enter the stock ticker symbol(s) and watch the visualizations!

## Future Improvements:

* Add support for multi-ticker analysis
* Include more technical indicators (e.g., MACD, Bollinger Bands)
* Integrate email notifications for critical price changes

---

Feel free to contribute to the project and suggest enhancements!
