# import os
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload

# # Define your credentials and scope
# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# def get_drive_service():
#     """Authenticate and return the Google Drive service."""
#     credentials = service_account.Credentials.from_service_account_file(
#         'path/to/your/service-account-key.json', scopes=SCOPES)
#     service = build('drive', 'v3', credentials=credentials)
#     return service

# def cloud_storege(instance, filename):
#     """ Implement a cloud storage solution using Google Drive. This function should perform the following tasks:
#     1. Upload a local file to the Google Drive.
#     2. Download a file from the Google Drive to a local directory.
#     3. Delete a file from the Google Drive.
#     """
#     """Uploads a file to Google Drive and returns the file's public URL."""
#     service = get_drive_service()
#     file_path = os.path.join('media', filename)
#     file_metadata = {'name': filename}
#     media = MediaFileUpload(file_path, resumable=True)
#     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     file_id = file.get('id')
#     service.permissions().create(
#         fileId=file_id,
#         body={'type': 'anyone', 'role': 'reader'}
#     ).execute()
#     file_url = f"https://drive.google.com/uc?id={file_id}&export=download"
#     return file_url

