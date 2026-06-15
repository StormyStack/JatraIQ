import os
import json
import logging
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

logger = logging.getLogger("google_sheets")

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_gspread_client() -> gspread.client.Client | None:
    """
    Authenticates and returns a gspread client.
    
    Attempts to load credentials from the GOOGLE_CREDENTIALS_JSON environment 
    variable first. If not found, falls back to the GOOGLE_CREDENTIALS_PATH file.
    
    Returns:
        gspread.client.Client: An authenticated Google Sheets client, or None on failure.
    """
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if credentials_json:
        try:
            creds_dict = json.loads(credentials_json)
            credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            return gspread.authorize(credentials)
        except Exception as e:
            logger.error(f"Failed to authorize Google Sheets client from GOOGLE_CREDENTIALS_JSON: {e}")
            return None

    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "google_credentials.json")
    if not os.path.exists(credentials_path):
        logger.error(f"Google credentials file not found at {credentials_path} and GOOGLE_CREDENTIALS_JSON is not set.")
        return None

    try:
        credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        return gspread.authorize(credentials)
    except Exception as e:
        logger.error(f"Failed to authorize Google Sheets client from file: {e}")
        return None

def update_google_sheet(df: pd.DataFrame) -> bool:
    """
    Appends a Pandas DataFrame to the target Google Spreadsheet.
    
    Initializes headers if the sheet is empty or headers are missing. 
    Applies custom formatting (frozen rows, background color) to headers.
    
    Args:
        df (pd.DataFrame): The data to append to the Google Sheet.
        
    Returns:
        bool: True if synchronization was successful, False otherwise.
    """
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        logger.error("GOOGLE_SHEET_ID not set in environment variables.")
        return False
        
    client = get_gspread_client()
    if not client:
        return False
        
    try:
        if "google.com" in sheet_id:
            spreadsheet = client.open_by_url(sheet_id)
        else:
            spreadsheet = client.open_by_key(sheet_id)
            
        worksheet = spreadsheet.sheet1
        
        df_filled = df.fillna("")
        headers = df_filled.columns.values.tolist()
        data_values = df_filled.values.tolist()
        
        existing_data = worksheet.get_all_values()
        is_empty = not existing_data or all(not any(row) for row in existing_data)
        
        header_format = {
            "backgroundColor": {"red": 0.0, "green": 0.33, "blue": 0.44},
            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 11},
            "horizontalAlignment": "CENTER"
        }
        
        if is_empty:
            worksheet.clear()
            worksheet.update(values=[headers] + data_values, range_name="A1")
            worksheet.freeze(rows=1)
            worksheet.format("1:1", header_format)
            logger.info(f"Successfully initialized and added data to Google Spreadsheet: {spreadsheet.title}")
        else:
            if existing_data[0] != headers:
                worksheet.insert_row(headers, index=1)
                worksheet.freeze(rows=1)
                worksheet.format("1:1", header_format)
                logger.info("Headers were missing. Inserted headers at row 1.")
                
            worksheet.append_rows(values=data_values)
            logger.info(f"Successfully appended {len(data_values)} rows to Google Spreadsheet: {spreadsheet.title}")
            
        return True
    except Exception as e:
        logger.error(f"Failed to update Google Spreadsheet: {e}")
        return False
