from datetime import datetime

import pytz


def get_now() -> datetime:
    return datetime.now(tz=pytz.UTC)
