import pandas as pd
from variables import EXCEL_FILENAME


def exe_generator(result: list[object],
                  referenced_column: str,
                  downloaded_column: str,
                  excel_sheetname: str,
                  excel_filename: str=EXCEL_FILENAME
                  ):
    """
    BUild the excel attendance report

    :param result: a list of the dowloaded data
    :type result: list[object]
    :param referenced_column: the refenrenced column we would used for the comparism eg 'index number'
    :type referenced_column: str
    :param downloaded_column: the downoaded column we would used for the comparism eg 'index number'
    :type result: str
    :param excel_sheetname: the sheet name we would be appending the final excel result to
    :type excel_sheetname: str
    :param excel_filename: the filename to the reference excel file
    :type excel_filename: str
    """
    try:
        # load the excelfile
        xlsx = pd.ExcelFile(excel_filename)
        # save all excels that where not processesd
        unprocessed_sheets = {}
        # check if the there exist the provided sheet
        if excel_sheetname in xlsx.sheet_names:
            # read a specific sheet
            df = pd.read_excel(excel_filename, sheet_name=excel_sheetname)
        else:
            # read the first sheet anyway
            df = pd.read_excel(excel_filename)
            
        print(df.columns)

        for i, data in enumerate(result):
            if data['status'] == 'success':
                # get the dataframe
                df_downloaded = data['df']

                # drop duplicates
                df_downloaded = df_downloaded.drop_duplicates()

                # make the column name unique so that we can
                # create and fill the attendance weekly
                col_name = f"{data['excelsheetID'][-3:]}:{str(i)}"
                df[col_name] = df[referenced_column].isin(df_downloaded[downloaded_column]).astype(int)
            else:
                col_name = f"{data['excelsheetID'][-3:]}:{str(i)}"
                unprocessed_sheets[col_name] = data

        # Save back into the same Excel file, replacing or adding a sheet 
        with pd.ExcelWriter(excel_filename, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer: 
            df.to_excel(writer, sheet_name=excel_sheetname, index=False)

        return {
                'status': 'success',
                'statusCode': 200,
                'message': 'attendance report has been generated successfully.',
                'unprocessed_sheets': unprocessed_sheets,
                'path_to_report': EXCEL_FILENAME
            }

    except Exception as e:
        # raise(e)
        return {
                'status': 'error',
                'statusCode': 500,
                'message': f"Error procesing and generating excel file: {str(e)}"
            }