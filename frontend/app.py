from flask import Flask
from main.routers import router as catalog_rt
from cart_routes.cart_rt import router as cart_rt

import requests

app = Flask(__name__)
app.register_blueprint(catalog_rt)
app.register_blueprint(cart_rt)
app.secret_key = "cab960a6b42ec5184326eeef4abb335f"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
