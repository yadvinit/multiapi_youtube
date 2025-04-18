# Multi API Youtube Videos Fetcher Model

This project is a Flask-based web application that fetches the **latest YouTube videos** based on a predefined search query/tag and stores them in a mongodb database. The server continuously polls the YouTube Data API at regular intervals (every 10 seconds), stores the video metadata, and provides a **paginated REST API** to access this data in reverse chronological order (latest first).

*****************************************************************************************************

## Files Descriptions

**app.py**

This is the **main file**. When you run this, it:
- Starts the Flask web server
- Starts a background thread to keep fetching videos from YouTube every 10 seconds

*****************************************************************************************************

**config.py**

This file holds your **configuration settings**, such as:
- Your YouTube API key
- The search term to look for
- The interval time (default 10 seconds)

*****************************************************************************************************

**.env**

This is a hidden file where you put **sensitive info**, like your YouTube API key and Mongo Uri. Example:
like=> YOUTUBE_API_KEY = asdfg,asdf,asdf

*****************************************************************************************************

**services/youtube_service.py**

- Calls the YouTube Data API
- Extracts useful info like title, description, published date, thumbnails, etc.
- Saves the video data into the database
- Makes sure no duplicate videos are saved

*****************************************************************************************************

**routes/main_routes.py**

- Creates a GET API route: /videos
- Accepts query parameters: page and limit
- Fetches video data from the database
- Sorts videos by published date in descending order (newest first)
- Returns the result as a JSON response

*****************************************************************************************************

**templates/home.html**

This is just a basic HTML file, if you want to show a simple homepage or message. It’s optional and not necessary for API use.

*****************************************************************************************************

**requirements.txt**

This file lists all the Python packages your app needs. You can install them using:

```bash
pip install -r requirements.txt


