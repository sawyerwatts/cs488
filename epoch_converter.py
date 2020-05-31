import time
import datetime

def convert_epoch(seconds, type="datetime"):
    if type == "string":
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds))
    elif type == "datetime":
        return datetime.datetime.fromtimestamp(time.mktime(time.localtime(seconds)))
    else:
        raise ValueError("'type' paremter takes 'datetime' or 'string'")

