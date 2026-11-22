from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
SCOPES=["https://www.googleapis.com/auth/youtube.upload"]
def upload(video_path,metadata,client_secret="client_secret.json"):
    if not Path(client_secret).is_file(): raise FileNotFoundError("Google OAuth Desktop credentials missing")
    flow=InstalledAppFlow.from_client_secrets_file(client_secret,SCOPES)
    creds=flow.run_local_server(port=0,access_type="offline",prompt="consent")
    yt=build("youtube","v3",credentials=creds)
    body={"snippet":{"title":metadata["title"],"description":metadata["description"],"tags":metadata.get("tags",[]),"categoryId":metadata.get("category_id","20")},"status":{"privacyStatus":metadata.get("privacy_status","private"),"selfDeclaredMadeForKids":False}}
    req=yt.videos().insert(part="snippet,status",body=body,media_body=MediaFileUpload(str(video_path),chunksize=-1,resumable=True))
    return "https://www.youtube.com/watch?v="+req.execute()["id"]
