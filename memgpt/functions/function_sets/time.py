from datetime import datetime
import pytz

def get_current_time_info(self, timezone: str = "Asia/Shanghai") -> str:
    """
    Returns the current date, time, timezone, location, and day of the week.

    Args:
        timezone (str): The timezone to get the current time for (default is 'Asia/Shanghai').

    Returns:
        str: A formatted string containing the current date, time, timezone, location, and day of the week.

    Example:
        current_time_info = get_current_time_info()
        print(current_time_info)
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = now.strftime("%A")
        location = timezone.split("/")[-1].replace("_", " ")

        return f"Location: {location}\nTime: {formatted_time}\nTimezone: {timezone}\nDay: {day_of_week}"
    except Exception as e:
        return f"Error: {str(e)}"