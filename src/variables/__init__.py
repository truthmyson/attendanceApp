import os

# async downoad limit
DOWNLOAD_LIMIT = 5

# response to be return from the server
RESPONSE = {
    'status': 'success',
    'body': {

    }
}

# part of the url string to be replaced
URL_FORMAT = 'edit?resourcekey='

# the refenrenced excelfile
EXCEL_FILENAME = os.path.abspath('src/report.xlsx')

print(EXCEL_FILENAME)