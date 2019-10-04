import json
from pandas.io.json import json_normalize
import dataset
import threading
from numpy import int64

import sendmail
import traceback


def serialize_list(j):
    jcp = {}
    for key in j:
        if type(j[key]) == list:
            if len(j[key]) == 0:
                pass
            elif len(j[key]) == 1:
                jcp[key] = j[key][0]
            else:
                for i in range(len(j[key])):
                    jcp['{}_{}'.format(key, i)] = j[key][i]
        elif type(j[key]) == dict:
            jcp[key] = serialize_list(j[key])
        else:
            jcp[key] = j[key]
    return jcp


def flatten(j: 'json'):
    j1 = serialize_list(j)
    j2 = json_normalize(j1, sep='$').iloc[0].to_dict()

    for key in j2:
        if type(j2[key]) == int64:
            j2[key] = j2[key].item()

        if j2[key] == False:
            j2[key] = 'False'
        elif j2[key] == True:
            j2[key] = 'True'
    return j2


class database:
    def __init__(self, db_str, table_str, *args, **kwargs):
        self.db = dataset.connect(db_str)

        if table_str not in self.db.tables:
            self.db.create_table(table_str, primary_id='pid')
        self.table = self.db[table_str]

    # pass the origin response json[item], the database will do the formatting
    def insert(self, j):
        try:
            assert type(j) == dict

            def insert_thread():
                flatten_j = flatten(j)
                self.table.insert(flatten_j)

            #t = threading.Thread(target = insert_thread)
            # t.start()

            insert_thread()
        except: 
            s = traceback.format_exc()
            sendmail.send(subject = 'Feedly Client Database.insert exception', 
                    body = json.dumps({
                        'exception': s, 
                        'j': j
                        }, ensure_ascii = False, indent = 4))

