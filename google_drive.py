import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Function to get files from Google Drive
def get_drive_files():
    # Authenticate using credentials stored in environment variables
    credentials, project = google.auth.load_credentials_from_file(os.getenv("GOOGLE_CREDENTIALS"))
    drive_service = build("drive", "v3", credentials=credentials)

    # Get the list of files from the specified folder in Google Drive
    folder_id = os.getenv("FOLDER_ID")
    query = f"'{folder_id}' in parents"
    results = drive_service.files().list(q=query).execute()
    files = results.get("files", [])

    return [file["name"] for file in files]
