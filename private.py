from googleapiclient.discovery import build

YOUTUBE_API_KEY = "AIzaSyB3fVYm6GJbQ6lodaKod0NhpKta1TzaBqo"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, cache_discovery=False)