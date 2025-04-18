from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
from datetime import datetime
from database import db
from dotenv import load_dotenv

load_dotenv()

def fetch_youtube_videos():
    
    print(f"[{datetime.now()}] Scheduled task: Fetching YouTube videos")
    
    api_keys = os.getenv("YOUTUBE_API_KEY", "").split(",")
    query = os.getenv("SEARCH_QUERY", "basketball")
    api_url = 'https://www.googleapis.com/youtube/v3/search'
    
    if not api_keys or api_keys[0] == "":
        print("No API keys configured")
        return
    
    # iterrating for each api
    for key_index, api_key in enumerate(api_keys):
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'order': 'date',
            'key': api_key,
            'maxResults': 10 
        }
        
        try:
            print(f"Using YouTube API key {key_index+1}/{len(api_keys)}")
            response = requests.get(api_url, params=params)
            
            if response.status_code == 403 and 'quotaExceeded' in response.text:
                print(f"API key {key_index+1} quota exceeded, trying next key")
                continue
                
            response.raise_for_status()
            data = response.json()
            items = data.get('items', [])
            
            # Format videos for storage
            videos = [
                {   
                    'query': query,
                    'videoId': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet'].get('description', ''),
                    'publishedAt': item['snippet']['publishedAt'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'channel': item['snippet']['channelTitle'],
                    'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'fetchedAt': datetime.utcnow().isoformat()
                }
                for item in items
            ]
            
            # storing to mongodb
            if videos:
                db.insert_videos(query, videos)
                print(f"Successfully stored {len(videos)} videos for query '{query}'")
            return
            
        except Exception as e:
            print(f"YouTube API error with key {key_index+1}: {str(e)}")
    
    print("All API keys failed")

def init_scheduler():
   
    scheduler = BackgroundScheduler()
    
    #job to fectch after 10 sec interval
    scheduler.add_job(
        fetch_youtube_videos,
        'interval', 
        seconds=10,
        id='fetch_youtube_videos'
    )
    
    scheduler.start()
    print("Scheduler started! Fetching YouTube videos every 10 seconds.")
    
    fetch_youtube_videos()
    
    return scheduler