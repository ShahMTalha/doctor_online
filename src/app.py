import os
from flask import Flask, send_from_directory
from src.models import db
from src.controllers import user_bp, doctor_bp, common_bp, patient_bp, lab_bp, ambulance_bp, store_bp

flask_app = Flask(__name__, static_url_path="", static_folder="src/static")
env_config = os.getenv("APP_SETTINGS", "src.config.DevelopmentConfig")
flask_app.config.from_object(env_config)

db.init_app(flask_app)
# migrate = Migrate(app, db)
flask_app.register_blueprint(user_bp, url_prefix='/users')
flask_app.register_blueprint(doctor_bp, url_prefix='/doctors')
flask_app.register_blueprint(common_bp, url_prefix='/common')
flask_app.register_blueprint(lab_bp, url_prefix='/lab')
flask_app.register_blueprint(patient_bp, url_prefix='/patient')
flask_app.register_blueprint(ambulance_bp, url_prefix='/ambulance')
flask_app.register_blueprint(store_bp, url_prefix='/store')

@flask_app.route("/")
def index():
    return "Welcome to flask app"

@flask_app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)
