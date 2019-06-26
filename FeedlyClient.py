import requests
import json
import sys
import urllib
import time
import random
from datetime import datetime


class FeedlyClient:
    def __init__(self, file_str, db, *args, **kwargs):
        self.file_str = file_str
        self.db = db
        self.prefix = 'https://cloud.feedly.com/v3'

        with open(file_str, 'r') as f:
            options = json.load(f)
        # print(options)

        self.client_id = options.get('client_id')
        self.client_secret = options.get('client_secret')
        self.access_token = options.get('access_token')
        self.refresh_token = options.get('refresh_token')
        self.last_fetch = options.get('last_fetch')
        self.my_stream_id1 = options.get('my_stream_id1')

    def tag_fetch(self):
        headers = self.auth_header()
        continuation = None

        total_fetched = 0

        while True:
            params = {'streamId': self.my_stream_id1,
                      'continuation': continuation,
                      'ranked': 'oldest',
                      'newerThan': self.last_fetch}

            res = self._get('/streams/contents',
                            params=params, headers=headers)

            total_fetched += len(res['items'])
            current_latest = -1
            for item in res['items']:
                self.db.insert(item)

                self.last_fetch = max(self.last_fetch, item['actionTimestamp'])
                current_latest = max(current_latest, item['actionTimestamp'])

            print('{} entries fetched, current latest {}!'.format(
                len(res['items']), datetime.fromtimestamp(current_latest/1000)))

            if 'continuation' not in res:
                break
            continuation = res['continuation']

            time.sleep(random.randint(2, 4))

        self.last_fetch += 1
        self._config_update('last_fetch', self.last_fetch)
        print('total {} entries fetched! latest {}'.format(
            total_fetched, datetime.fromtimestamp(self.last_fetch/1000)))

        return total_fetched

    def _get(self, endpoint, params=None, headers=None):
        path = self.prefix + endpoint
        r = requests.get(path, params=params, headers=headers)

        if r.status_code == 401:
            self._renew_access_token()
            headers['Authorization'] = self.auth_header()['Authorization']
            return self._get(endpoint, params, headers)

        try:
            r.raise_for_status()
        except:
            print(r.json(), flush=True, file=sys.stderr)
            raise

        return r.json()

    def auth_header(self):
        return {'Authorization': 'Bearer {}'.format(self.access_token)}

    def _renew_access_token(self):
        data = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }

        r = requests.post(self.prefix+'/auth/token', data=data)

        try:
            r.raise_for_status()
        except:
            print(r.json(), flush=True, file=sys.stderr)
            raise

        jr = r.json()
        self.access_token = jr['access_token']
        self._config_update('access_token', self.access_token)

        print('access_token is successfully updated',
              flush=True, file=sys.stderr)

    def _config_update(self, entry, updated_value):
        with open(self.file_str, 'r') as f:
            options = json.load(f)
        options[entry] = updated_value
        with open(self.file_str, 'w') as f:
            json.dump(options, f)
