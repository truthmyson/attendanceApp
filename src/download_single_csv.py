import pandas as pd
from aiohttp import ClientSession
import asyncio
from variables import DOWNLOAD_LIMIT
import io

async def download_single_csv(
            Session: ClientSession,
            url: str,
            col_to_drop: list[str]
            ) -> object:
    """
    Download a single excelsheet as csv file

    :param session: http session odject to make request
    :type session: aiohttp.ClientSession
    :param url: url of the excelsheet to download
    :type url: str
    :param col_to_drop: the columns to drop
    :type col_to_drop: list[str]
    :return: metadata object of each excel sheet
    :rtype: object
    """
    statusCode = 500
    # url processing
    # split the url to get the name of the column
    if '/edit?gid=' in url:
        url = url.replace('/edit?gid=', '/export?format=csv&gid=').split(",")
        col_name = url[-1].strip() if len(url) > 1 else None
        url = url[0].split("#gid=")[0].strip()
    else:
        url = url.replace('edit?resourcekey=', 'export?format=csv').split(",")
        col_name = url[-1].strip() if len(url) > 1 else None
        url = url[0].strip()


    # limit downloads at a time using shared semaphore
    async with asyncio.Semaphore(DOWNLOAD_LIMIT):
        try:
            async with Session.get(url, timeout=10, allow_redirects=True) as response:
                # get the data as bytes
                data = await response.text()
                response.raise_for_status() # raise any error response
                statusCode = response.status

                try:
                    # use StringIO synchronously (not an async context manager)
                    csv_file = io.StringIO(data)
                    df = pd.read_csv(csv_file)
                    
                    # drop unwanted column
                    if len(col_to_drop) > 0:
                        df = df.drop(columns=[*col_to_drop])

                    return {
                        'status': 'success',
                        'excelsheetID': url.split('gid=')[-1],
                        'df': df,
                        'col_name': col_name
                    }
                except Exception as e:
                    return {
                    'status': 'error',
                    'message': f"Error streaming the csv file: {str(e)}",
                    'statusCode': statusCode,
                    'excelsheetID': url.split('gid=')[-1]
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error downloading the excelsheet: {str(e)}",
                'statusCode': statusCode,
                'excelsheetID': url.split('gid=')[-1],
                'url': url
            }
