from flask import Flask
from flask_cors import CORS
from endpoints.base import base_bp
from endpoints.reference_excel import reference_excel_bp
from endpoints.generate_report import generate_report_bp
from endpoints.get_report_path import get_report_path_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    app.register_blueprint(base_bp)
    app.register_blueprint(reference_excel_bp)
    app.register_blueprint(generate_report_bp)
    app.register_blueprint(get_report_path_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)