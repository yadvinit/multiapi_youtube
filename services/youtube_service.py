from flask import current_app
from database import db

def get_recent_videos(query, page=1, per_page=None):
   
    if per_page is None:
        per_page = current_app.config['RESULTS_PER_PAGE']
    
    skip = (page - 1) * per_page
    
    # getting from monogdb
    videos, total_count = db.get_videos_paginated(
        query, 
        skip=skip,
        limit=per_page
    ) 
    
    print(f"Found {total_count} total videos for query '{query}', returning {len(videos)} videos")
    has_next = (skip + per_page) < total_count
    has_prev = page > 1
    
    return {
        'videos': videos,
        'page': page,
        'total': total_count,
        'has_next': has_next,
        'has_prev': has_prev,
        'next_page': page + 1 if has_next else None,
        'prev_page': page - 1 if has_prev else None,
        'cached': True
    }