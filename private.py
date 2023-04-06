from googleapiclient.discovery import build

#AIzaSyCW9tUGpTcL84Q3DuaqWmeQ2DCV4Ycycqc
#AIzaSyB3fVYm6GJbQ6lodaKod0NhpKta1TzaBqo
YOUTUBE_API_KEY = "AIzaSyCW9tUGpTcL84Q3DuaqWmeQ2DCV4Ycycqc"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, cache_discovery=False)