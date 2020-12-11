
import requests, json, secrets

def pretty(data):
    if type(data) is str:
        print(data)
    elif type(data) is dict.dict_keys:
        print(list(data))
    else:
        print(json.dumps(data, sort_keys=True, indent=4))

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

def delete_reddit_token():
    cache_dict = load_cache()
    cache_dict.pop("reddit_token")
    write_cache(cache_dict)

def get_reddit_token():
    cache_dict = load_cache()
    if "reddit_token" in cache_dict:
        return cache_dict["reddit_token"]
    else:
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
        cache_dict["reddit_token"] = token
        write_cache(cache_dict)
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
        "include_facets": True
    }
    return requests.get(api_url, headers=headers, params=params).json()

if __name__ == "__main__":
    token = get_reddit_token()
    pretty(reddit_search("qanon", token)["data"]["children"][0].keys())
    # https://boards.4chan.org/search#/qanon