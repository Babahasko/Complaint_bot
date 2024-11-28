def get_surveillance_from_list_by_name(user_surveillances, search_surveillance_name):
    all_surveillance_names = [surveillance["name"] for surveillance in user_surveillances]
    if search_surveillance_name in all_surveillance_names:
        return user_surveillances[all_surveillance_names.index(search_surveillance_name)]
    else:
        return None

def get_surveillance_from_list_by_enumerate_index(user_surveillances, search_surveillance_number):
    try:
        search_surveillance_number = int(search_surveillance_number)
    except (ValueError, TypeError):
        return None
    list_of_surveillances = [[index + 1, surveillance] for index, surveillance in enumerate(user_surveillances)]
    all_surveillance_enumerate_numbers = [surveillance[0] for surveillance in list_of_surveillances]
    if search_surveillance_number in all_surveillance_enumerate_numbers:
        return user_surveillances[all_surveillance_enumerate_numbers.index(search_surveillance_number)]
    else:
        return None

def get_enumerate_list_of_surveillances_with_id(user_surveillances):
    list_of_surveillances = [[index + 1, surveillance] for index, surveillance in enumerate(user_surveillances)]
    return list_of_surveillances

def get_pretty_enumerate_list_of_surveillances(user_surveillances):
    list_of_surveillances = [[index + 1, surveillance] for index, surveillance in enumerate(user_surveillances)]
    text = f""
    for surveillance in list_of_surveillances:
        text += f"{surveillance[0]}. {surveillance[1]["name"]}\n"
    return text
