import pandas as pd
import gspread

import gsheets_credentials


def upload_pandas(df, spreadsheet_key, wks_name):
    """ upload pandas DF to Google sheets
    """
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = gsheets_credentials.get_credentials(scope)
    gc = gspread.authorize(credentials)
    work_sheet = gc.open_by_key(spreadsheet_key).worksheet(wks_name)
    work_sheet.update([df.columns.values.tolist()] + df.values.tolist())


def download_pandas(spreadsheet_key, wks_name):
    """ download pandas DF from Google sheets
    """
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = gsheets_credentials.get_credentials(scope)
    gc = gspread.authorize(credentials)
    work_sheet = gc.open_by_key(spreadsheet_key).worksheet(wks_name)
    dataframe = pd.DataFrame(work_sheet.get_all_records())
    return dataframe

