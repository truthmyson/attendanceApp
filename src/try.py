# from multi_csv_download import multi_csv_download
# from exe_generator import exe_generator
import asyncio
from main import main
from pprint import pprint


# try it out
if __name__ == '__main__':

    payload = {}
    urls = [
        'https://docs.google.com/spreadsheets/d/1PEGLTMaVzt-Ed2DWHPCjWHVVtlPyWMqERtGh40S-_zQ/edit?resourcekey=&gid=1269987887#gid=1269987887',
        'https://docs.google.com/spreadsheets/d/1PEGLTMaVzt-Ed2DWHPCjWHVVtlPyWMqERtGh40S-_zQ/edit?resourcekey=&gid=285255461#gid=285255461',
        'https://docs.google.com/spreadsheets/d/1PEGLTMaVzt-Ed2DWHPCjWHVVtlPyWMqERtGh40S-_zQ/edit?resourcekey=&gid=1260299904#gid=1260299904',
        '://docs.google.com/spreadsheets/d/1PEGLTMaVzt-Ed2DWHPCjWHVVtlPyWMqERtGh40S-_zQ/edit?resourcekey=&gid=1260299904#gid=1260299904'
    ]
    payload['urls'] = urls
    payload['ref_exe'] = ''
    payload['col_to_drop'] = ['first name', 'last name']
    payload['reference_col'] = 'INDEX'
    payload['downloaded_col'] = 'index number'
    payload['excel_sheetname'] = 'automata'

    response = asyncio.run(main(payload))
    pprint(response)



    # urls = [
    #     'https://docs.google.com/spreadsheets/d/1PEGLTMaVzt-Ed2DWHPCjWHVVtlPyWMqERtGh40S-_zQ/edit?resourcekey=&gid=1269987887#gid=1269987887',
    #     'https://docs.google.com/spreadsheets/d/1PEGLTMaVzt-Ed2DWHPCjWHVVtlPyWMqERtGh40S-_zQ/edit?resourcekey=&gid=285255461#gid=285255461',
    #     'https://docs.google.com/spreadsheets/d/1PEGLTMaVzt-Ed2DWHPCjWHVVtlPyWMqERtGh40S-_zQ/edit?resourcekey=&gid=1260299904#gid=1260299904'
    # ]
    # response = asyncio.run(multi_csv_download(urls))
    # result = exe_generator(response['result'],'INDEX', 'index number','math')
    
    # print(result)