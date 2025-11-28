# Google Sheets Integration Setup Guide

## Overview
Your A2A project now has full Google Sheets integration with a dedicated `sheets_agent` that can read, write, append, and manage spreadsheet data.

## Installation Requirements

Install the required Google API packages:

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Authentication Setup

### Option 1: Service Account (Recommended for automated workflows)

1. **Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project

2. **Enable Google Sheets API:**
   - In the Cloud Console, go to APIs & Services > Library
   - Search for "Google Sheets API"
   - Click "Enable"

3. **Create a Service Account:**
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "Service Account"
   - Fill in the details and click "Create and Continue"
   - Skip optional steps and finish

4. **Create a Key:**
   - Go to the service account details
   - Click "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON"
   - A JSON file will download - save this securely

5. **Set Environment Variable:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

6. **Share Spreadsheets:**
   - Share any Google Sheets you want to access with the service account email (found in the JSON file under "client_email")

## Usage

### Basic Functions

Use these custom functions directly or through the `sheets_agent`:

#### Read from Google Sheets
```python
from custom_functions import read_google_sheet

data = read_google_sheet(
    spreadsheet_id="your-spreadsheet-id",
    range_name="Sheet1!A1:D10"
)
print(data)
```

#### Write to Google Sheets
```python
from custom_functions import write_google_sheet

values = [
    ["Name", "Age", "City"],
    ["John", "30", "NYC"],
    ["Jane", "28", "LA"]
]

response = write_google_sheet(
    spreadsheet_id="your-spreadsheet-id",
    range_name="Sheet1!A1:C3",
    values=values
)
```

#### Append to Google Sheets
```python
from custom_functions import append_to_google_sheet

new_rows = [
    ["Bob", "35", "Chicago"]
]

response = append_to_google_sheet(
    spreadsheet_id="your-spreadsheet-id",
    range_name="Sheet1!A:C",
    values=new_rows
)
```

#### Clear Data
```python
from custom_functions import clear_google_sheet

response = clear_google_sheet(
    spreadsheet_id="your-spreadsheet-id",
    range_name="Sheet1!A:C"
)
```

#### Get Spreadsheet Metadata
```python
from custom_functions import get_sheet_metadata

metadata = get_sheet_metadata("your-spreadsheet-id")
print(metadata["sheets"])  # List all sheets in the spreadsheet
```

### Using the Sheets Agent

The root agent now has access to the sheets_agent as a sub-agent:

```python
from agent import root_agent

# The agent can now handle Google Sheets requests
response = root_agent.run("Read all data from Sheet1 in spreadsheet [ID]")
```

## Finding Your Spreadsheet ID

The spreadsheet ID is in the URL of your Google Sheet:
```
https://docs.google.com/spreadsheets/d/YOUR-SPREADSHEET-ID/edit
                                     ^^^^^^^^^^^^^^^^^^^^^^^^
```

## File Structure

- `google_sheets_utils.py` - Core Google Sheets API wrapper with `GoogleSheetsConnector` class
- `custom_functions.py` - Enhanced with Google Sheets functions
- `custom_agents.py` - New `sheets_agent` specialized for spreadsheet operations
- `agent.py` - Updated root agent with sheets_agent integration

## Advanced Usage

### Creating a New Spreadsheet
```python
from google_sheets_utils import get_sheets_connector

connector = get_sheets_connector()
spreadsheet_id = connector.create_spreadsheet(
    title="My New Sheet",
    sheet_names=["Data", "Analysis", "Reports"]
)
print(f"Created spreadsheet: {spreadsheet_id}")
```

### Batch Operations
```python
from custom_functions import read_google_sheet, append_to_google_sheet

# Read existing data
data = read_google_sheet("spreadsheet-id", "Sheet1!A:C")

# Process and append new data
processed_data = [[row[0].upper(), row[1], row[2]] for row in data]
append_to_google_sheet("spreadsheet-id", "Sheet1!A:C", processed_data)
```

## Troubleshooting

- **Authentication Error**: Ensure `GOOGLE_APPLICATION_CREDENTIALS` env var is set correctly
- **Permission Denied**: Make sure the service account email has been granted access to the spreadsheet
- **Range Errors**: Double-check sheet names and range syntax (e.g., "Sheet1!A1:D10")
- **Import Errors**: Verify all required packages are installed with pip

## Security Notes

- Never commit service account credentials to version control
- Use environment variables or secure vaults for credential paths
- Grant minimal necessary permissions to service accounts
- Regularly rotate service account keys
