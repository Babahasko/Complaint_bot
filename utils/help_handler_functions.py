def get_theme_from_list_by_name(user_themes, search_theme_name):
    all_theme_names = [theme["name"] for theme in user_themes]
    if search_theme_name in all_theme_names:
        return user_themes[all_theme_names.index(search_theme_name)]
    else:
        return None

def get_theme_from_list_by_enumerate_index(user_themes, search_theme_number):
    try:
        search_theme_number = int(search_theme_number)
    except (ValueError, TypeError):
        return None
    list_of_themes = [[index + 1, theme] for index, theme in enumerate(user_themes)]
    all_theme_enumerate_numbers = [theme[0] for theme in list_of_themes]
    if search_theme_number in all_theme_enumerate_numbers:
        return user_themes[all_theme_enumerate_numbers.index(search_theme_number)]
    else:
        return None

def get_enumerate_list_of_themes_with_id(user_themes):
    list_of_themes = [[index + 1, theme] for index, theme in enumerate(user_themes)]
    return list_of_themes

def get_pretty_enumerate_list_of_themes(user_themes):
    list_of_themes = [[index + 1, theme] for index, theme in enumerate(user_themes)]
    text = f""
    for theme in list_of_themes:
        text += f"{theme[0]}. {theme[1]["name"]}\n"
    return text
