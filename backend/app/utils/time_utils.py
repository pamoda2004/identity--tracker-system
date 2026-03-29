from datetime import datetime

def timestamp_str() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")