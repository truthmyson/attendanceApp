from flask import Blueprint, request, jsonify
from exe_generator import exe_generator
from multi_csv_download import multi_csv_download


generate_report_bp = Blueprint('generate_report', __name__)


@generate_report_bp.route('/generate-report', methods=['POST'])
async def generate_report():
    # Ensure request is JSON
    if not request.is_json:
        return jsonify({
            "status": "error",
            "statuscode": 400,
            "message": "Request must be JSON"
        })

    data = request.get_json()

    # Required fields for this endpoint
    required_fields = ['downloaded_col', 'excel_sheetname', 'reference_col', 'col_to_drop', 'urls']
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
    if not isinstance(data['downloaded_col'], str):
        errors.append("'downloaded_col' must be a string")
    if not isinstance(data['excel_sheetname'], str):
        errors.append("'excel_sheetname' must be a string")
    if not isinstance(data['reference_col'], str):
        errors.append("'reference_col' must be a string")
    if not isinstance(data['col_to_drop'], list) or not all(isinstance(col, str) for col in data['col_to_drop']):
        errors.append("'col_to_drop' must be a list of strings")
    if not isinstance(data['urls'], list) or not all(isinstance(url, str) for url in data['urls']):
        errors.append("'urls' must be a list of strings")

    if errors:
        return jsonify({
            "status": "error",
            "statuscode": 400,
            "message": "; ".join(errors)
        })

    try:
        # our result holder
        result = {'body': {}}

        # download the atendance using the links
        download_urls = await multi_csv_download(data['urls'], data['col_to_drop'])

        # generate the exelfile
        generate_exe = exe_generator(
            download_urls['result'],
            data['reference_col'],
            data['downloaded_col'],
            data['excel_sheetname']
            )
        
        # generate the reponse base on status value
        if download_urls['status'] == 'error':
            result['downloading_urls_metadata'] = download_urls

        if generate_exe['status'] == 'error':
            result['report_metadata'] = generate_exe
        else:
            result['body']['unprocessed_sheets'] = generate_exe['unprocessed_sheets']
            result['body']['path_to_report'] = generate_exe['path_to_report']
            result['message'] = 'Attendance report generated successfully.'
            
        result['status'] = 'success'
        result['statuscode'] = 200

        return jsonify(result)
    except Exception as e:
        raise(e)
        # return jsonify({
        #     'status': 'error',
        #     'statuscode': 500,
        #     'message': f'Error calling worker: {str(e)}'
        # })