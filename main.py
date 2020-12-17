
import requests, json, secrets, sqlite3, csv, sys
import pandas as pd
from bs4 import BeautifulSoup

def pretty(data):
    if type(data) is str:
        print(data)
    elif type(data) is dict or type(data) is list:
        print(json.dumps(data, sort_keys=True, indent=4))
    else:
        print(list(data))

def load_cache():
    try:
        with open("cache.json") as cache_file:
            return json.load(cache_file)
    except:
        return {}

def write_cache(cache_dict):
    with open("cache.json", "w") as cache_file:
        json.dump(cache_dict, cache_file)

def get_html(url):
    cache_dict = load_cache()
    if url in cache_dict:
        print("Using cache...")
        return cache_dict[url]
    else:
        html = requests.get(url).text
        cache_dict[url] = html
        write_cache(cache_dict)
        print("Fetching...")
        return html

def get_api_data(url, params={}):
    cache_dict = load_cache()
    cache_key_str = "reddit:"
    if cache_key_str in cache_dict and False:
        print("Using cache...")
        return cache_dict[cache_key_str]
    else:
        api_data_dict = requests.get(url, params=params).json()
        cache_dict[cache_key_str] = api_data_dict
        write_cache(cache_dict)
        print("Fetching...")
        return api_data_dict

def get_reddit_token():
    headers = {
        "User-agent": "qanon-app 0.1"
    }
    params = {
        "grant_type": "password",
        "username": "cubaiceland",
        "password": "jordanfi"
    }
    auth = ("uoXP3F2Qh1cjrQ", secrets.REDDIT_API_KEY)
    auth_response = requests.post("https://www.reddit.com/api/v1/access_token", headers=headers, params=params, auth=auth).json()
    token = auth_response["access_token"]
    return token

def reddit_search(q, token):
    api_url = "https://oauth.reddit.com/search" #and the rest
    headers = {
        "Authorization": "bearer " + token,
        "User-agent": "qanon-app 0.1"
    }
    params = {
        "q": q,
        "type": "link",
        "sr_detail": False,
        "include_facets": True,
        "sort": "top",
        "t": "day",
        "limit": 100
    }
    return requests.get(api_url, headers=headers, params=params).json()

def get_nyt_article():
    article_url = "https://www.nytimes.com/2020/10/15/technology/youtube-bans-qanon-violence.html"
    html = get_html(article_url)
    soup = BeautifulSoup(html, 'html.parser')
    article_text = soup.find(name="section", attrs={"name": "articleBody"}).get_text()
    return article_text


def create_db():
    conn = sqlite3.connect("app-data.db")
    try:
        conn.execute("DROP TABLE PewData")
    except:
        None
    print("Creating new PewData table...")
    conn.execute("CREATE TABLE PewData (YTNEWS text, YTNEWSIMP text, YTACT text, YTCHANNELLOYAL text, YTNEWS2 text, YTSKEP TEXT, YTRECSSAT text)")
    conn.commit()

    with open("pew-data.csv", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            conn.execute(f"INSERT INTO PewData VALUES ('{row['YTNEWS_W59']}', '{row['YTNEWSIMP_W59']}', '{row['YTACT_W59']}', '{row['YTCHANNELLOYAL_W59']}', '{row['YTNEWS2_W59']}', '{row['YTSKEP_W59']}', '{row['YTRECSSAT_W59']}')")
            conn.commit()

def print_survey_responses(response_dict, user_response):
    total = 0
    for response, count in response_dict.items():
        total += count
    user_response_count = response_dict[user_response]
    print(f"Wow! {round(user_response_count/total*100)}% of survey respondents said the same thing!\n")
    print('Below are the stats for all survey respondents:')
    for response, count in response_dict.items():
        print(f'{response}: {round(count/total*100)}%')

def get_user_response(response_dict):
    responses = list(response_dict.keys())
    for index, response in enumerate(responses):
        print(f"{index + 1}. {response}")
    user_response = input("Please pick a number: ")
    while not user_response.isnumeric() or int(user_response) not in range(1, len(responses)+1):
        user_response = input("Please enter a valid number: ")
    chosen_response = responses[int(user_response) - 1]
    return chosen_response

def yt_survey():
    conn = sqlite3.connect("app-data.db")
    survey_answers = {}
    columns = ["YTNEWS", "YTNEWSIMP", "YTACT", "YTCHANNELLOYAL", "YTNEWS2", "YTSKEP", "YTRECSSAT"]
    for row in conn.execute("SELECT * FROM PewData"):
        for index, response in enumerate(row):
            column_name = columns[index]
            if response == "" or response == "Refused":
                continue
            if column_name not in survey_answers:
                survey_answers[column_name] = {}
            if response in survey_answers[column_name]:
                survey_answers[column_name][response] += 1
            else:
                survey_answers[column_name][response] = 1
    
    #pretty(survey_answers)
    print("Question 1: Do you ever get news from YouTube videos? By news we mean current events and issues.")
    user_response = get_user_response(survey_answers["YTNEWS"])
    print_survey_responses(survey_answers["YTNEWS"], user_response)
    print()
    print("Question 2: How important to you, if at all, are YouTube videos as a way of keeping up with the news?")
    user_response = get_user_response(survey_answers["YTNEWSIMP"])
    print_survey_responses(survey_answers["YTNEWSIMP"], user_response)
    print()
    print("Question 3: How often, if at all, do you interact with YouTube news videos through actions like commenting, liking or disliking, subscribing, or sharing?")
    user_response = get_user_response(survey_answers["YTACT"])
    print_survey_responses(survey_answers["YTACT"], user_response)
    print()
    print("Question 4: Which of the following statements comes closer to your view when it comes to YouTube news videos?")
    user_response = get_user_response(survey_answers["YTCHANNELLOYAL"])
    print_survey_responses(survey_answers["YTCHANNELLOYAL"], user_response)
    print()
    print("Question 5: When you watch news videos on YouTube, do you also watch the recommended news videos that appear alongside the video you are watching?")
    user_response = get_user_response(survey_answers["YTNEWS2"])
    print_survey_responses(survey_answers["YTNEWS2"], user_response)
    print()
    print("Question 6: Which of the following best describes how you approach YouTube news videos, even if neither is exactly right? ")
    user_response = get_user_response(survey_answers["YTSKEP"])
    print_survey_responses(survey_answers["YTSKEP"], user_response)
    print()
    print("Question 7: How good of a job does YouTube do at recommending news videos for you?")
    user_response = get_user_response(survey_answers["YTRECSSAT"])
    print_survey_responses(survey_answers["YTRECSSAT"], user_response)
    print()



if __name__ == "__main__":
    print("///////////////////////////////////////TOP QANON POSTS CREATED TODAY ON REDDIT///////////////////////////////////////////////")
    token = get_reddit_token()
    top_reddit_list = reddit_search("qanon", token)["data"]["children"]
    post_list = []
    for item in top_reddit_list:
        condensed = {
            "title": item["data"]["title"],
            "subreddit": item["data"]["subreddit"],
            "url": item["data"]["url"],
            "score": item["data"]["score"]
        }
        post_list.append(condensed)
    print("Printing Top 5 Qanon Reddit Posts Created Today")

    for index, post_dict in enumerate(post_list[:5]):  #enumerate takes list, gives index in ordered fashion 
        print (f'{index + 1}. {post_dict["title"]}\nSCORE: {post_dict["score"]}\nLINK: {post_dict["url"]}\n')
    
    aggregate_upvotes_int = sum([x["score"] for x in post_list])
    print(f'Aggregate Upvotes for Top 100 Qanon Posts Created Today: {aggregate_upvotes_int}')
    print()
    print("///////////////////////////////////////NEW YORK TIMES ARTICLE ON QANON///////////////////////////////////////////////")
    print(get_nyt_article())
    print()
    print("///////////////////////////////////////AGGREGATING YOUTUBE USER SENTIMENT ON NEWS SOURCES///////////////////////////////////////////////")
    #df = pd.read_spss("pew-data.sav")
    #df.to_csv("pew-data.csv")
    print("CREATING DATABASE FROM CSV DATASET... THIS COULD TAKE A WHILE (30 - 60 seconds)...")
    create_db()
    yt_survey()
    #pretty(top_reddit_list[0]["data"].keys())

