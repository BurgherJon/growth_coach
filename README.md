# Growth Mindset Coach

A daily growth mindset coaching application built on Google's Gemini AI models that helps users stay focused on developing a growth mindset through personalized coaching sessions. The application records coaching interactions and maintains progress notes in a Google Sheet for ongoing reference and development tracking.

## Overview

This Growth Mindset Coach provides:
- Daily personalized coaching conversations focused on growth mindset principles
- Automatic recording of coaching sessions and insights to Google Sheets
- Reference to previous coaching notes to maintain continuity and track progress
- Built-in Google search capabilities for enhanced coaching resources
- Configurable AI models for different coaching scenarios

## Features

- **Personalized Coaching**: Uses high-quality AI models for meaningful coaching conversations
- **Progress Tracking**: Automatically logs coaching sessions to Google Sheets
- **Historical Context**: References past coaching sessions for continuity
- **Search Integration**: Incorporates relevant resources through Google search
- **Flexible Configuration**: Supports different AI models for various coaching needs

## Project Structure

```
growth_coach/
├── agent.py                 # Main growth coach agent
├── custom_agents.py         # Google search agent
├── custom_functions.py      # Google Sheets integration functions
├── sheet_utilities.py       # Google Sheets API utilities
├── .env                     # Environment variables (not in repo)
├── credentials/             # Google service account credentials (not in repo)
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- Google Cloud Project with required APIs enabled
- Google Sheets API access
- Service account with appropriate permissions

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd growth_coach
```

### 2. Install Dependencies

```bash
pip install python-dotenv google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 3. Google Cloud Setup

1. **Create a Google Cloud Project** (if you don't have one)
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Required APIs**
   ```bash
   gcloud services enable sheets.googleapis.com
   gcloud services enable drive.googleapis.com
   ```

3. **Create a Service Account**
   - Go to IAM & Admin > Service Accounts in Google Cloud Console
   - Click "Create Service Account"
   - Give it a name (e.g., "growth-coach-service")
   - Grant it "Editor" role or create custom role with Sheets/Drive permissions
   - Download the JSON key file

4. **Set up Google Sheets**
   - Create a new Google Sheet for coaching notes
   - Share the sheet with your service account email (found in the JSON key file)
   - Give it "Editor" permissions
   - Note the sheet ID from the URL (the long string between `/d/` and `/edit`)

### 4. Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=your-location-source
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-google-api-key

# AI Model Configuration... you can use two different models if you prefer.  Choose from these models: https://ai.google.dev/gemini-api/docs/models
HIGH_QUALITY_AGENT_MODEL=
QUICK_AGENT_MODEL=

# Google Sheets Integration.  You will need to setup a service account and give it access to a sheet that you'll use for the Growth Coach's notes and then store the key for that account (see next step).
# Then you will need to specify the ID of the growth coach's Google sheet.  You can find this in the URL of the sheet. It is the long string of letters and numbers after "/d/" and before "/edit".
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
GROWTH_COACH_SSID=the-id-of-your-growth-coaches-googlesheet

```

### 5. Credentials Setup

1. **Save Service Account Key**
   - Create a `credentials/` directory in your project
   - Place your downloaded JSON key file in this directory
   - Update the `GOOGLE_APPLICATION_CREDENTIALS` path in `.env` to point to this file

2. **Load Environment Variables**
   - The application uses `python-dotenv` to load environment variables
   - Ensure your Python files include:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Usage

1. **Start a Coaching Session**
   ```bash
   adk web
   ```

2. **View Coaching History**
   - Check your configured Google Sheet to see logged coaching sessions
   - Each session includes date, coaching notes, and progress insights

## File Descriptions

- **`agent.py`**: Main coaching agent that conducts growth mindset conversations
- **`custom_agents.py`**: Contains specialized agents including Google search functionality
- **`custom_functions.py`**: Functions for reading/writing coaching data to Google Sheets
- **`sheet_utilities.py`**: Google Sheets API connection and utility functions

## Troubleshooting

### Common Issues

1. **"Credentials not found" Error**
   - Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to a valid JSON file
   - Verify the service account has proper permissions
   - Check that the file path is correct (relative to project root)

2. **Google Sheets Permission Denied**
   - Verify the service account email has been shared with your Google Sheet
   - Ensure the service account has "Editor" permissions on the sheet
   - Double-check the `GROWTH_COACH_SSID` matches your sheet ID

3. **API Key Issues**
   - Verify your `GOOGLE_API_KEY` is valid and has Gemini API access enabled
   - Check that billing is enabled on your Google Cloud project
