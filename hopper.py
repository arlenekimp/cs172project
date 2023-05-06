import requests
from keys import r_client_id, r_client_secret, r_password, r_user_agent, r_username
import re

# this uses reddit api rather than praw but it uses the same credentials so no need to change keys or any of the data under here
# to access the reddit api
auth = requests.auth.HTTPBasicAuth(r_client_id, r_client_secret)
data = {
    'grant_type': 'password',
    'username': r_username,
    'password': r_password
}
headers = {'User-Agent': 'MyAPI/0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth = auth,
                    data = data,
                    headers = headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

# --------------------- DEBUGGING ---------------------
# code under should print <Response [200]> if accessing api was successful
# print(requests.get('https://oauth.reddit.com/api/v1/me', headers = headers))

# reddit api documentation: https://www.reddit.com/dev/api/oauth

# srname is the name of the subreddit
# cs is the checked_subreddit list
# ns is the new_subreddit list that hasn't been checked through
def hopper(srname, cs, ns):
    # stops if the subreddit was already checked
    if srname in cs:
        return cs
    res = requests.get(f'https://oauth.reddit.com/r/{srname}/about', headers = headers)
    checked_subs = cs
    checked_subs.append(srname)
    new_subs = ns
    # try loop is when the subreddit doesn't contain suggested subreddits to look through
    try:
        desc = res.json()['data']['description'].lower()
        relindex = desc.find("subreddits")
        relpast = desc[relindex:]
        s = relpast.split("r/")
        for i in s:
            cleaned = re.sub(r'[^a-zA-Z0-9]', '', i)    # max subreddit name length is 21 characters
            if (len(cleaned) <= 21) & (cleaned not in checked_subs) & (cleaned != "subreddits") & (cleaned != ""):
                new_subs.append(cleaned)
    except Exception as e:
        print("This subreddit had no related subreddits in description")
        return (checked_subs, new_subs)
    return (checked_subs, new_subs)

# runs a sample of the hopper function and creates a subreddit_list.jsonl file containing subreddits
#  related to the main subreddit
srname = "foodhacks"    # main subreddit
checked_subs = []       # subreddits that have been checked
new_subs = []           # new subreddits in the list
checked_subs, new_subs = hopper(srname, checked_subs, new_subs)

numhops = 6             # number of hops sometimes leads to an insanely large amount even at 2 so set max to numhops^2
for i in new_subs:
    checked_subs, new_subs = hopper(i, checked_subs, new_subs)
    if(len(new_subs) > numhops * numhops):
        break
    # print(checked_subs)
    # print(new_subs)

f = open("subreddit_list.jsonl", "w")
for sub in new_subs:
    f.write(sub + "\n")
f.close()