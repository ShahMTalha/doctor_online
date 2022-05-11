from src.app import flask_app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    flask_app.debug = False
    flask_app.run('0.0.0.0', port=port)