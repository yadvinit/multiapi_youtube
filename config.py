import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # youtube API settings
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "").split(",")
    YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'
    DEFAULT_SEARCH_QUERY = os.getenv("SEARCH_QUERY", "basketball")
    RESULTS_PER_PAGE = 10