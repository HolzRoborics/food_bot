from datetime import datetime


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

    current_day = num_to_day[datetime.today().weekday()]
    if current_day in food.name:
        return True
    else:
        return False
