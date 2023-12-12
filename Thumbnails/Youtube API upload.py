# Youtube API upload

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

def upload_video():
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "Description of uploaded video.",
                "title": "Test video upload"
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": "2023-11-19T16:25:05.0Z",
                "selfDeclaredMadeForKids": False, 
            }
        },
        media_body=MediaFileUpload("YOUR_VIDEO_FILE_PATH")
    )
    response = request.execute()

    print(response)

    video_id = response['id']

    # Upload thumbnail
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload('YOUR_THUMBNAIL_FILE_PATH')
    ).execute()