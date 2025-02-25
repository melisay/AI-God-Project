from flask import Flask

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
except ImportError:
    print("Ensure flask_limiter is installed: pip install Flask-Limiter")

# Flask app setup
app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
)
