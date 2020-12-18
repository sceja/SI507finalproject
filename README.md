# Final Python Project - Aggregating Disinformation via Qanon 

Libraries, please install: requests, pandas, BeautifulSoup
* Pandas is only used for converting the pew-data to csv - respective code will be commented out.

Reddit API key can be accessed via secrets.py uploaded to canvas. 
* Please put secrets.py at the top level of this project. 

To execute the code use command `python3 main.py`

When running the code three things will happen:
* Top 10 QAnon posts on Reddit get displayed to the user as well as the aggregate score of the top 100 QAnon posts via the official Reddit API. 
* Scraped and Cached New York Times article detailing a QAnon 101 for the user. 
* Interactive survey on YouTube user sentiment pertaining using social media sites as legible news sources. The users responses are recorded and matched with data `https://www.pewresearch.org/politics/datasets/`. The specific data is ATW_59. The original data format was pew-data.sav and used pandas to convert to csv. Each time the program runs, it reads the csv file and creates a new database. 