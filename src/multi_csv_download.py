from download_single_csv import download_single_csv
from aiohttp import ClientSession
import asyncio
from time import localtime, strftime

async def multi_csv_download(
            urls: list[str],
            col_to_drop: list[str]=['first name', 'last name']
            ) -> object:
    """
    Multi-excelsheet downloading

    :param urls: list of excelsheet urls
    :type urls: list[str]
    :param col_to_drop: the columns to drop
    :type col_to_drop: list[str]
    :return: metadata object
    :rtype: object
    """
    statusCode = 500
    try:
        async with ClientSession() as Session:
            # create threads for tasks
            tasks = [asyncio.create_task(download_single_csv(Session, url, col_to_drop)) for url in urls]
            # gather all the results
            result = await asyncio.gather(*tasks)
            now = strftime("%Y-%m-%d %H:%M:%S", localtime())

            return {
                'status': 'success',
                'statuscode': 200,
                'timestamp': now,
                'result': result
            }
    except Exception as e:
        return {
                'status': 'error',
                'message': f"Error multi downloading the excelsheets: {str(e)}",
                'statusCode': statusCode,
            }
