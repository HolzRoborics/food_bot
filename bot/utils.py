import datetime


def get_date():
    """
    Order before 10:30 - today
    after 10:30 - tomorrow
    """
    current_time = datetime.datetime.now()
    result_datetime = current_time + datetime.timedelta(hours=13, minutes=30)
    return result_datetime.date()


def food_filter(food: 'FoodModel'):
    num_to_day = {
        0: 'понед',
        1: 'вторн',
        2: 'сред',
        3: 'четв',
        4: 'пятн',
        5: 'субб',
        6: 'воскр',
    }
    for text_day in num_to_day.values():
        if text_day in food.name:
            break
    else:
        return True

    current_day = num_to_day[get_date().weekday()]
    if current_day in food.name:
        return True
    else:
        return False


def generate_order_uid(user_id: int):
    date = datetime.datetime.now().strftime("%m%d%f")
    return int(f'{date}{user_id}')
