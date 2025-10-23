# app.py
from flask import Flask, jsonify
from routes.stock_routes import stock_bp  # we'll create this file next

def create_app():
    app = Flask(__name__)

    # Register all route blueprints
    app.register_blueprint(stock_bp)

    # Root endpoint (shows available endpoints)
    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to the Stock Info API",
            "endpoints": {
                "/stock/<symbol>": "Get stock data (e.g., /stock/AAPL)",
                "/stocks?symbols=AAPL,MSFT,GOOG": "Get multiple stocks at once"
            }
        })

    # Example 404 handler (customizes error response)
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
