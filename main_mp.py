import praw
import json
import re
import requests
import time
import concurrent.futures
import multiprocessing as mp
from urllib.request import urlopen
from bs4 import BeautifulSoup

from keys import r_client_id, r_client_secret, r_password, r_user_agent, r_username

#chmod +x <filename>
#./crawler.sh <subreddit>
# subreddit_name = sys.argv[1]

def crawler(subreddit_name):
    reddit = praw.Reddit(
        client_id= r_client_id,
        client_secret= r_client_secret,
        password= r_password,
        user_agent= r_user_agent,
        username= r_username,
        #read_only=True
    )
    print(f"Crawling subreddit: {subreddit_name}")

    file_num = 1
    top = reddit.subreddit(subreddit_name).top(limit=None)

    with open(f"posts_{file_num}_{subreddit_name}.jsonl", "w") as f:
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
                "urlLink": []
            })
            post.comments.replace_more(limit=None)
            for comment in post.comments.list():
                data["comments"].append(comment.body)
                permalink = comment.permalink 
                # check if comment body contains a URL
                urls = re.findall("(?P<url>https?://[^\s]+)", comment.body)
                data["urlLink"].append(urls)
                for url in urls:
                    try:
                        print(url)
                        html_page = urlopen(url, timeout=10)
                        soup = BeautifulSoup(html_page, "html.parser")
                        title = soup.title.string.strip()
                        data["urlNames"].append(title)
                    except Exception as e:
                    # store an error message or flag in the JSON data for this URL
                        data["urlNames"].append({"error": str(e)})
                        # skip if error
                        #pass
                    
                #     print(f"Title: {title}")
                #     print(f"Description: {description}")
                #     print(f"Image URL: {image_url}")
            
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
            print("I am successful!: {}".format(subreddit_name))

def main():
    print("Please wait . . .")
    #
    #
    #   DISCLAIMER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #
    # Add subreddits here as a string of arrays
    subreddits = ["sub1", "sub2", "sub3", "sub4", "sub5", "sub6", "sub7", "sub8"] # eight
    
    print("Subreddit list created!")
    print("======================")
    print("Start crawling!")
    
    #processes = []

    # Create a new process for each subreddit and start it
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exec:
        exec.map(crawler, subreddits)
    #for subreddit in subreddits:
    #    process = mp.Process(target=crawler, args=(subreddit,))
    #    process.start()
    #    processes.append(process)

    # Wait for all processes to finish
    #for process in processes:
    #    process.join()

    end_time = time.time()
    print(f"Total time elapsed: {end_time - start_time}")
    print("Completed!")
    #with mp.Pool(8) as p:
    #    p.map(crawler, subreddits)

if __name__ == '__main__':
    main()