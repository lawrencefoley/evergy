from datetime import date, timedelta


def get_past_date(days_back: int = 1) -> date:
    """
    Get a date based on a number of days back from today
    :rtype: date
    :param days_back: The number of days back to get the date for
    :return: The date in the past
    """
    return date.today() - timedelta(days=days_back)
