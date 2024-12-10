import locale
from datetime import datetime

months = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

def reformat_data(str_data:str) -> str:
    date_obj = datetime.fromisoformat(str_data)
    formatted_date = f"{date_obj.day} {months[date_obj.month]} {date_obj.year} {date_obj.hour}:{date_obj.minute}:{date_obj.second}"
    return formatted_date

def get_complain_from_list_by_enumerate_index(user_complains, search_complain_number):
    try:
        search_complain_number = int(search_complain_number)
    except (ValueError, TypeError):
        return None
    list_of_complains = [[index + 1, complain] for index, complain in enumerate(user_complains)]
    all_complain_enumerate_numbers = [complain[0] for complain in list_of_complains]
    if search_complain_number in all_complain_enumerate_numbers:
        search_result = user_complains[all_complain_enumerate_numbers.index(search_complain_number)]
        data = search_result["data"]
        search_result["readable_data"] = reformat_data(data)
        return user_complains[all_complain_enumerate_numbers.index(search_complain_number)]
    else:
        return None

def get_enumerate_list_of_complains_with_id(user_complains):
    list_of_complains = [[index + 1, complain] for index, complain in enumerate(user_complains)]
    return list_of_complains

def get_pretty_enumerate_list_of_complains(user_complains):
    list_of_complains = [[index + 1, complain] for index, complain in enumerate(user_complains)]
    text = f""
    for complain in list_of_complains:
        data_str = complain[1]["data"]
        readable_data = reformat_data(data_str)
        text += f"{complain[0]}. {complain[1]["surveillance"]} {complain[1]["theme"]} {readable_data}\n"
    return text
