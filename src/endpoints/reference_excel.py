from flask import Blueprint, request, jsonify
from add_reference_exe import add_reference_exe

reference_excel_bp = Blueprint('reference_excel', __name__)


@reference_excel_bp.route('/reference-excel', methods=['POST'])
def reference_excel():
    # Ensure request is JSON
    if not request.is_json:
        return jsonify({
            "status": "error",
            "statuscode": 400,
            "message": "Request must be JSON"
        }), 400

    data = request.get_json()

    # Required fields for this endpoint
    required_fields = ['ref_exe', 'col_to_drop']
    errors = []

    # Check presence
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing field: '{field}'")

    if errors:
        return jsonify({
            "status": "error",
            "statuscode": 400,
            "message": "; ".join(errors)
        })

    # Validate types
    ref_exe = data['ref_exe']
    col_to_drop = data['col_to_drop']

    if not isinstance(ref_exe, str):
        errors.append("'ref_exe' must be a string. (An encoded excel file.)")
    if not isinstance(col_to_drop, list) or not all(isinstance(col, str) for col in col_to_drop):
        errors.append("'col_to_drop' must be a list of strings. (A list of unwanted columns.)")

    if errors:
        return jsonify({
            "status": "error",
            "statuscode": 400,
            "message": "; ".join(errors)
        })
    try:
        # send request to te worker
        response = add_reference_exe(data['ref_exe'], data['col_to_drop'])

    
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'statuscode': 500,
            'message': f'Error calling Reference worker: {str(e)}'
        })