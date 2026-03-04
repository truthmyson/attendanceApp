from flask import Blueprint, jsonify

base_bp = Blueprint('base', __name__)

@base_bp.route('/', methods=['GET'])
def index():

    # response with metadata about the applycation
    return jsonify({
        "status": "success",
        "statuscode": 200,
        "api_version": "1.0.0",
        "message": "Attendance report generator is running.",
        "endpoints": {
            "/": {
                "method": "Get",
                "description": "This help message.",
            },
            "/get_report_path": {
                "method": "Get",
                "description": "Get the path to the generated report file.",
            },
            "/reference-excel": {
                "method": "POST",
                "description": "Validates reference Excel data",
                "required_fields": ["ref_exe", "col_to_drop"]
            },
            "/generate-report": {
                "method": "POST",
                "description": "Generates a report from given URLs and columns",
                "required_fields": ["urls", "downloaded_col", "excel_sheetname", "reference_col", "col_to_drop"]
            }
        }
    })
