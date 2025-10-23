# services/stock_service.py

import yfinance as yf
import pandas_ta as ta  # optional (for RSI or other indicators)

def fetch_stock_summary(symbol):
    """
    Fetch a single stock's latest data and return a summary dictionary.
    """
    symbol = symbol.upper()
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="5d")  # use 5 days to ensure data exists

    if data.empty:
        return None

    # Use last available trading day
    last = data.iloc[-1]
    price = last["Close"]
    open_price = last["Open"]
    high = last["High"]
    low = last["Low"]
    volume = int(last["Volume"])

    # Calculate percent change (fix parentheses)
    change_percent = ((price - open_price) / open_price) * 100

    # Optional: calculate RSI (using pandas_ta)
    try:
        rsi_series = ta.rsi(data["Close"], length=14)
        rsi = float(rsi_series.dropna().iloc[-1]) if not rsi_series.dropna().empty else None
    except Exception:
        rsi = None

    # Insight text
    if change_percent > 0:
        insight = "stock is moving upward"
    elif change_percent == 0:
        insight = "stock is stable"
    else:
        insight = "stock is moving downward"

    return {
        "Symbol": symbol,
        "Price": round(price, 2),
        "Open": round(open_price, 2),
        "High": round(high, 2),
        "Low": round(low, 2),
        "Volume": volume,
        "ChangePercent": round(change_percent, 2),
        "RSI": round(rsi, 2) if rsi else None,
        "Insight": insight
    }


def fetch_multiple_stocks(symbol_list):
    """
    Fetch summaries for multiple symbols at once.
    """
    results = []
    for symbol in symbol_list:
        summary = fetch_stock_summary(symbol)
        if summary:
            results.append(summary)
        else:
            results.append({"Symbol": symbol.upper(), "error": "No data found"})
    return results
