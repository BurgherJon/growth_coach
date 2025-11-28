"""
Google Sheets utilities for connecting to Google Sheets API.
"""

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import os
from typing import List, Dict, Any, Optional


class GoogleSheetsConnector:
    """Manages connection to Google Sheets API."""
    
    def __init__(self, credentials_path: Optional[str] = None, scopes: Optional[List[str]] = None):
        """
        Initialize Google Sheets connector.
        
        Args:
            credentials_path: Path to service account credentials JSON file.
                            If None, uses GOOGLE_APPLICATION_CREDENTIALS env var.
            scopes: List of OAuth scopes. Defaults to Sheets and Drive scopes.
        """
        self.scopes = scopes or [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Get credentials path
        if credentials_path is None:
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError(
                f"Credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS "
                f"env var or pass credentials_path parameter."
            )
        
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=self.scopes
        )
        
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
    
    def read_sheet(self, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
        """
        Read data from a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet.
            range_name: The range to read (e.g., 'Sheet1!A1:D10').
        
        Returns:
            List of rows from the sheet.
        """
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        return result.get('values', [])
    
    def write_sheet(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]) -> Dict[str, Any]:
        """
        Write data to a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet.
            range_name: The range to write to (e.g., 'Sheet1!A1:D10').
            values: 2D list of values to write.
        
        Returns:
            Response from the API.
        """
        body = {
            'values': values
        }
        
        result = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        return result
    
    def append_sheet(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]) -> Dict[str, Any]:
        """
        Append data to a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet.
            range_name: The range to append to (e.g., 'Sheet1!A:D').
            values: 2D list of values to append.
        
        Returns:
            Response from the API.
        """
        body = {
            'values': values
        }
        
        result = self.sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        return result
    
    def clear_sheet(self, spreadsheet_id: str, range_name: str) -> Dict[str, Any]:
        """
        Clear data from a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet.
            range_name: The range to clear (e.g., 'Sheet1!A1:D10').
        
        Returns:
            Response from the API.
        """
        result = self.sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        return result
    
    def get_spreadsheet_metadata(self, spreadsheet_id: str) -> Dict[str, Any]:
        """
        Get metadata about a spreadsheet including sheet names.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet.
        
        Returns:
            Spreadsheet metadata.
        """
        result = self.sheets_service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()
        
        return result
    
    def create_spreadsheet(self, title: str, sheet_names: Optional[List[str]] = None) -> str:
        """
        Create a new Google Sheet.
        
        Args:
            title: Title for the new spreadsheet.
            sheet_names: Optional list of sheet names to create.
        
        Returns:
            The ID of the created spreadsheet.
        """
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        
        if sheet_names:
            spreadsheet['sheets'] = [
                {'properties': {'title': name}} for name in sheet_names
            ]
        
        result = self.sheets_service.spreadsheets().create(
            body=spreadsheet
        ).execute()
        
        return result['spreadsheetId']


# Global connector instance (initialized on demand)
_connector = None


def get_sheets_connector(credentials_path: Optional[str] = None) -> GoogleSheetsConnector:
    """Get or create a Google Sheets connector instance."""
    global _connector
    if _connector is None:
        _connector = GoogleSheetsConnector(credentials_path)
    return _connector
