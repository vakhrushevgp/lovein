import datetime
import json


class DataBase:
    def __init__(self, file):
        self.file = file

    def add(self, post_id, info):
        post_id = str(post_id)
        with open(self.file) as json_file:
            data = json.load(json_file)
            data[post_id] = info
        with open(self.file, "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def update(self, post_id, count):
        post_id = str(post_id)
        with open(self.file) as json_file:
            data = json.load(json_file)
            if post_id in data:
                data[post_id][2] = count
        with open(self.file, "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def day(self):
        most_id, most_count = 0, 0
        with open(self.file) as json_file:
            data = json.load(json_file)
            for post_id in data:
                if data[post_id][0] == datetime.datetime.now().month:
                    if data[post_id][1] == datetime.datetime.now().day:
                        if data[post_id][2] >= most_count:
                            most_count = data[post_id][2]
                            most_id = post_id
        return most_id

    def month(self):
        most_id, most_count = 0, 0
        cur_month = datetime.datetime.now().month
        with open(self.file) as json_file:
            data = json.load(json_file)
            for post_id in data:
                if data[post_id][0] == cur_month:
                    if data[post_id][2] >= most_count:
                        most_count = data[post_id][2]
                        most_id = post_id
        self.clear(cur_month)
        return most_id

    def clear(self, cur_month):
        with open(self.file) as json_file:
            data = dict(json.load(json_file))
            old_keys = []
            for post_id in data:
                if not (-1 <= data[post_id][0] % 12 - cur_month % 12 <= 1):
                    old_keys.append(post_id)
            for key in old_keys:
                data.pop(key)
        with open(self.file, "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
