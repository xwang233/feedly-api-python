import traceback
import json

import FeedlyClient
import DataBase

import sendmail # my customized sendmail module


def main():
    db = DataBase.database('sqlite:///feedly.db', 'feedly')

    fdc = FeedlyClient.FeedlyClient('config.json', db)

    fdc.tag_fetch()


if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        s = traceback.format_exc()
        sendmail.send(subject='Feedly client exception at main', body = s)

