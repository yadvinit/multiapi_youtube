import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.videos_collection = None
        self.connect()

    def connect(self):
       
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable not set")
        
        # ssl connection
        self.client = MongoClient(mongo_uri, tlsAllowInvalidCertificates=True)
        self.db = self.client.youtube_data
        self.videos_collection = self.db.videos
        
        # creating indexes in mongo
        self.videos_collection.create_index([("query", 1)])
        self.videos_collection.create_index([("publishedAt", -1)])
        self.videos_collection.create_index([("query", 1), ("videoId", 1)], unique=True)

    def insert_videos(self, query, videos):
        """Store videos in MongoDB"""
        for video in videos:
            video["query"] = query  
            self.videos_collection.update_one(
                {"query": query, "videoId": video["videoId"]},
                {"$set": video},
                upsert=True
            )
        return len(videos)
    
    def get_videos(self, query, page_token=None, limit=10):
        """Legacy method - kept for backwards compatibility"""
        skip = 0
        if page_token and page_token.isdigit():
            skip = int(page_token)
        
        return self.get_videos_paginated(query, skip, limit)
    
    def get_videos_paginated(self, query, skip=0, limit=10):
        """Get videos from MongoDB with pagination using skip/limit"""
        videos = list(self.videos_collection.find(
            {"query": query},
            {'_id': 0}  
        ).sort("publishedAt", -1).skip(skip).limit(limit))
        
        # Get total count for pagination
        total_count = self.videos_collection.count_documents({"query": query})
        
        return videos, total_count

# database instance
db = Database()