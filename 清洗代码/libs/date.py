from datetime import datetime

def update_time():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')   # 时间格式要求未知