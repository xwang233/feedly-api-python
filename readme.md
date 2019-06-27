# Feedly-API-Python

This is a Python script that I used to fetch my saved articles (now Boards) on feedly.com. 

## Prerequisites 

Python 3, requests, pandas, numpy (pandas and numpy are used to flatten json). 

## Usage 

1. Download the source files. 
2. Create a *config.json* file, which contains your secret tokens and looks like 
```json
{
    "client_id": "XXX", 
    "client_secret": "XXX", 
    "access_token": "XXX", 
    "refresh_token": "XXX", 
    "last_fetch": -1, 
    "my_stream_id1": "user/XXX"
}
```

- You may apply for a [developer access token](https://developer.feedly.com/v3/developer/), 
or find them using the web app (feedly.com) with Chrome developer tools. Check API calls in Network tab.  

- The `my_stream_id1` is the streamId you will need. 
For each "saved article category" (now Board) you would like to fetch, there is a `streamId`. 
The `streamId` can be achieved through an [API call](https://developer.feedly.com/v3/tags/), 
or using the Chrome developer tools. 

- If you have more than one category to fetch, 
modify the `FeedlyClient.tag_fetch()` function and the `streamId` parameters in it. 

- This script fetches your saved articles incrementally, 
the `last_fetch` is the timestamp of the most recent fetch, and it is checked during each run. 
The format is unix timestamp in millisecond. 
For your first time "incremental fetch", which is actually a "full fetch", you may set that as `-1`. 

3. For the database, I used the [Python dataset](https://dataset.readthedocs.io/en/latest/) library. 
As an example, I used SQLite backend with it. 
If you would like to use other kinds of library, make sure your DataBase wrapper support a 
`DataBase.insert(item: json)` method. 
The only argument is the item dict from the original response json. 
```
full response (json) -> response['items'] (list) -> item (json)
```
- The `DataBase.insert` method is responsible to format the `item-json` and store that into 
the database. 
- Each `item` is a saved article with many metadata. 

4. Run `python3 main.py`. Wait until the fetch finishes. 

5. Enjoy! File issue or PR if you have any suggestions.

## License 

MIT. Use at your own risk. 
