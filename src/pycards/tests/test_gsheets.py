from pycards.gsheets import download_gsheets


def test_download_gsheets():
    SHEET_ID = "1Q8gs-XEURbsVB43OSe1DDL_W3T7tPryzOr-oUkxydbE"
    SHEET_NAME = "Master"
    df = download_gsheets(SHEET_ID, SHEET_NAME)
    assert len(df) > 0
