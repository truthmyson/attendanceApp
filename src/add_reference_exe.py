import base64
import pandas as pd
import io
import os
from variables import EXCEL_FILENAME

def add_reference_exe(encoded_data: str, filename: str=EXCEL_FILENAME) -> object:
    """
    save the refenrence excel data

    :param encoded_data: Base64 encoded string of the referenced Excel file.
    :type encoded_data: str
    :param filename: the filename for saving (e.g., 'report.xlsx').
    :type filename: str
    :return: metadata object of file location
    :rtype: object
    """
    try:
        # Step 1: Decode the base64 string into bytes
        decoded_bytes = base64.b64decode(encoded_data)

        # Step 2: Stream the bytes into memory and read as Excel
        with io.BytesIO(decoded_bytes) as excel_stream:
            df = pd.read_excel(excel_stream)

            # Step 4: Save it into excel
            df.to_excel(filename, index=False)

        # get absolute path
        file_path = os.path.abspath(filename)
        EXCEL_FILENAME = file_path

        return {
            'status': 'success',
            'status': 'success',
            'statuscode': 200,
            'ref_filepath': file_path,
        }
    except Exception as e:
        return {
                'status': 'error',
                'message': f"Error saving the refenrence excel file: {str(e)}",
                'statusCode': 500,
            }