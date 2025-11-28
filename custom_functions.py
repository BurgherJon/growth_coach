import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from .sheet_utilities import get_sheets_connector


# Google Sheets functions
def get_yesterdays_results() -> Dict[str, Any]:
        """
        Retrieve the row from Sheet1 containing yesterday's date.

        Reads all data from Sheet1 in the spreadsheet specified by the
        GROWTH_COACH_SSID environment variable, then finds and returns
        the row where the "Date" column matches yesterday's date
        (in YYYY-MM-DD format).

        Returns:
                Dictionary mapping column names to values for yesterday's row,
                or an empty dict if no matching row found.
        """
        # Get spreadsheet ID from environment variable
        spreadsheet_id = os.getenv('GROWTH_COACH_SSID')
        if not spreadsheet_id:
                raise ValueError("GROWTH_COACH_SSID environment variable not set")
        
        # Get yesterday's date in YYYY-MM-DD format
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Read all data from Sheet1
        connector = get_sheets_connector()
        rows = connector.read_sheet(spreadsheet_id, 'Sheet1!A:Z')
        
        if not rows or len(rows) < 2:
                return {}  # No data or only headers
        
        # First row is headers
        headers = rows[0]
        
        # Find the "Date" column index
        try:
                date_column_index = headers.index('Date')
        except ValueError:
                raise ValueError("'Date' column not found in Sheet1")
        
        # Search for the row with yesterday's date
        for row in rows[1:]:  # Skip header row
                if len(row) > date_column_index and row[date_column_index] == yesterday:
                        # Found the matching row, convert to dict
                        return {headers[i]: row[i] if i < len(row) else '' for i in range(len(headers))}
        
        # No matching row found
        return {}


def append_growth_coach_entry(
        Today_Date: str,
        Yesterday_Hard_Task_Reflection: str,
        Slobby_Reflection: str,
        Today_Hard_Task: str
) -> Dict[str, Any]:
        """
        Append a new row to the growth coach spreadsheet.

        Adds a new entry to Sheet1 in the spreadsheet specified by the
        GROWTH_COACH_SSID environment variable with the provided values.

        Args:
                Today_Date: The date for this entry (e.g., '2025-11-27').
                Yesterday_Hard_Task_Reflection: Reflection on yesterday's hard task.
                Slobby_Reflection: Reflection on today's slobby behavior.
                Today_Hard_Task: The hard task for today.

        Returns:
                Response from the API confirming the append operation.
        """
        # Get spreadsheet ID from environment variable
        spreadsheet_id = os.getenv('GROWTH_COACH_SSID')
        if not spreadsheet_id:
                raise ValueError("GROWTH_COACH_SSID environment variable not set")
        
        # Create the row with values in the specified order
        new_row = [
                Today_Date,
                Yesterday_Hard_Task_Reflection,
                Slobby_Reflection,
                Today_Hard_Task
        ]
        
        # Append the row to Sheet1
        connector = get_sheets_connector()
        return connector.append_sheet(spreadsheet_id, 'Sheet1!A:D', [new_row])


