import praw
import json
import re
import requests
from bs4 import BeautifulSoup

from keys import r_client_id, r_client_secret, r_password, r_user_agent, r_username

reddit = praw.Reddit(
    client_id= r_client_id,
    client_secret= r_client_secret,
    password= r_password,
    user_agent= r_user_agent,
    username= r_username,
)

file_num = 1
top = reddit.subreddit("restaurants").top(limit=25)

with open("data_collection.jsonl", "w") as f:
    file_size = 0
    for post in top: 
        data = ({
            "id": post.id,
            "title": post.title,
            "body": post.selftext,
            "username": str(post.author),
            "upvotes": post.score,
            "url": post.url,
            "permalink": post.permalink, 
            "comments": [],
            "urlNames": [],
            "urlDesc": [],
            "imageURL": []
        })
        post.comments.replace_more(limit=None)
        for comment in post.comments:
            data["comments"].append(comment.body)
            permalink = comment.permalink 
            # check if comment body contains a URL
            urls = re.findall("(?P<url>https?://[^\s]+)", comment.body)
            for url in urls:
                # Send GET request to URL and parse the HTML
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # extract info
                title = soup.title.string
                description = soup.find("meta", property="og:description")["content"] if soup.find("meta", property="og:description") else ""

                image_url = soup.find("meta", property="og:image")["content"] if soup.find("meta", property="og:image") else ""

                data["urlNames"].append(title)
                data["urlDesc"].append(description)
                data["imageURL"].append(image_url)
                
                #print(f"Title: {title}")
                print(f"Description: {description}")
                print(f"Image URL: {image_url}")
        
        json_str = json.dumps(data)
        row_size = len(json_str) + 1  
        if file_size + row_size > 10 * 1024 * 1024:
            # If adding this row exceeds the file size limit, close current file and open a new one
            f.close()
            file_num += 1
            f = open(f"reddit_{file_num}.jsonl", "w")
            file_size = 0
        f.write(json_str)
        f.write("\n")
        file_size += row_size