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

# reddit = praw.Reddit(
#     client_id="N3quc_HTtVYONqPMcTavvg",
#     client_secret="c7CgOu7FGZJg_uBa5NfuTH6vlo5Hbg",
#     password="Tyson12@",
#     user_agent="Comment Extraction (by u/USERNAME)",
#     username="carrotsa",
# )

# client_id=N3quc_HTtVYONqPMcTavvg
# client_secret=c7CgOu7FGZJg_uBa5NfuTH6vlo5Hbg
# user_agent=Comment Extraction (by u/USERNAME)
# username=carrotsa 
# password=Tyson12@

subreddit = reddit.subreddit('restaurants')
top_subreddit = subreddit.new(limit=25)
words_collection = []

for submission in top_subreddit:
    title = submission.title
    title_words = title.split()
    words_collection.append(title_words)

print(words_collection)


# with open("data.json", "w") as outfile:
#     json.dump(data, outfile)