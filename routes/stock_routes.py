# routes/stock_routes.py

from flask import Blueprint, jsonify, request
from services.stock_service import fetch_stock_summary, fetch_multiple_stocks

# Blueprint lets you group related routes together
stock_bp = Blueprint("stock", __name__)

# -----------------------------
# GET /stock/<symbol>
# -----------------------------
@stock_bp.route("/stock/<symbol>", methods=["GET"])
def get_stock(symbol):
    try:
        result = fetch_stock_summary(symbol)
        if result is None:
            return jsonify({"error": f"No data found for symbol {symbol}"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# GET /stocks?symbols=AAPL,MSFT,GOOG
# -----------------------------
@stock_bp.route("/stocks", methods=["GET"])
def get_stocks():
    symbols = request.args.get("symbols", "")
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]

    if not symbol_list:
        return jsonify({"error": "No symbols provided"}), 400

    try:
        results = fetch_multiple_stocks(symbol_list)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
