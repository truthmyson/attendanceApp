from add_reference_exe import add_reference_exe
from multi_csv_download import multi_csv_download
from exe_generator import exe_generator


async def main(payload: object) -> object:
    """
    centralise the workers on producing report

    :param payload: the json data
    :type payload: onject
    :return: metadata on workers
    :rtype: object
    """
    try:
        # our result holder
        result = {}
        # change the reference excel file
        if len(payload['ref_exe']) > 10:
            ref_file = add_reference_exe(payload['ref_exe'])

        # download the atendance using the links
        download_urls = await multi_csv_download(payload['urls'],payload['col_to_drop'])

        # generate the exelfile
        generate_exe = exe_generator(
            download_urls['result'],
            payload['reference_col'],
            payload['downloaded_col'],
            payload['excel_sheetname']
            )
        
        if len(payload['ref_exe']) > 10:
            if ref_file['status'] == 'error':
                result['ref_file_metadata'] = ref_file

        if download_urls['status'] == 'error':
            result['downloading_urls_metadata'] = download_urls

        if generate_exe['status'] == 'error':
            result['report_metadata'] = generate_exe
        else:
            result['unprocessed_sheets'] = generate_exe['unprocessed_sheets']
            result['path_to_report'] = generate_exe['path_to_report']
            
        result['status'] = 'success'
        result['statuscode'] = 200

        return result
    except Exception as e:
        return {
                'status': 'Error',
                'message': f"Error calling workers: {str(e)}",
                'statusCode': 500,
            }    