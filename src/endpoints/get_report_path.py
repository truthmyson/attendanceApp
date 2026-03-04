from flask import Blueprint, jsonify
from variables import EXCEL_FILENAME

get_report_path_bp = Blueprint('get_report_path', __name__)

@get_report_path_bp.route('/get_report_path', methods=['GET'])
def get_report_path():

    # return path to report
    return jsonify({
        "status": "success",
        "statuscode": 200,
        "body": {
            "report_path": EXCEL_FILENAME
        }
    })