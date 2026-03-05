from flask import Blueprint, jsonify, send_file
from variables import EXCEL_FILENAME
import os

get_report_path_bp = Blueprint('get_report_path', __name__)

@get_report_path_bp.route('/get_report_path', methods=['GET'])
def download_report():
    """Download the latest report file."""
    return send_file(EXCEL_FILENAME, as_attachment=True)

@get_report_path_bp.route('/report_info', methods=['GET'])
def report_info():
    """Return information about the latest report (filename only)."""
    try:
        filename = os.path.basename(EXCEL_FILENAME)
        return jsonify({
            "status": "success",
            "statuscode": 200,
            "body": {
                "filename": filename
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "statuscode": 500,
            "message": str(e)
        })