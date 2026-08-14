from datetime import datetime
from zoneinfo import ZoneInfo


def get_timezone(timezone_name):
    """
    Return the current datetime for the given timezone.
    """
    try:
        return datetime.now(ZoneInfo(timezone_name))
    except Exception as error:
        print(f"Timezone error: {error}")
        return None