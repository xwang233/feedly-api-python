import traceback
import json

import FeedlyClient
import DataBase


def main():
    db = DataBase.database('sqlite:///feedly.db', 'feedly')

    fdc = FeedlyClient.FeedlyClient('config.json', db)

    fdc.tag_fetch()


if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
