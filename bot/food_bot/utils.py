import datetime


def get_date():
    """
    Order before 10:30 - today
    after 10:30 - tomorrow
    """
    current_time = datetime.datetime.now()
    result_datetime = current_time + datetime.timedelta(hours=13, minutes=30)
    return result_datetime.date()
