# Tag Matters Dashboard

![screenshot_v1](https://github.com/rimhoho/tag-matters/blob/master/static/images/Screenshot.png)
[Link to Deployed Project](https://tag-matters.herokuapp.com/)
- Top 10 tags generated from the New York Times dashboard along with Google Search and YouTube videos
- An example of creating a data pipeline that can stream potentially GBs of data from an external API into a PostgreSQL database.

### Goal
- To understand how the large data gathered and stored into Postgres from Flask
- To see which frequently used tags are captured by New York Times and how people react about the topic by looking at other media platforms

### Data
- New York Times API: https://developer.nytimes.com/apis
- Pytrends API - Unofficial Google Search Trends API: https://pypi.org/project/pytrends/#interest-over-time
- Youtube API: https://developers.google.com/youtube/v3/docs/search/list?hl=en_US

### References
- SQLAlchemy with ETL : https://www.freecodecamp.org/news/sqlalchemy-makes-etl-magically-easy-ab2bd0df928/
- Flask by Example : https://github.com/bswiss/D3_Heroku_App
- Explore what the world is searching : https://trends.google.com/trends/?geo=US
