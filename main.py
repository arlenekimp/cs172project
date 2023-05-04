import praw
import json

from keys import r_client_id, r_client_secret, r_password, r_user_agent, r_username

reddit = praw.Reddit(
    client_id= r_client_id,
    client_secret= r_client_secret,
    password= r_password,
    user_agent= r_user_agent,
    username= r_username,
)

# subreddit = reddit.subreddit('restaurants')
# top_subreddit = subreddit.new(limit=25)
# words_collection = []

# for submission in top_subreddit:
#     title = submission.title
#     title_words = title.split()
#     words_collection.append(title_words)

# print(words_collection)

#words_collection = []

top = reddit.subreddit("restaurants").top(limit=500)
#data_collection = [ ]


with open("data_collection.jsonl", "w") as f:
    for post in top: 
        data = ({
            "id": post.id,
            "title": post.title,
            "body": post.selftext,
            "username": str(post.author),
            "upvotes": post.score,
            "url": post.url,
            "permalink": post.permalink 
        })
        f.write(json.dumps(data))
        f.write("\n")
    #data_collection.append(data)