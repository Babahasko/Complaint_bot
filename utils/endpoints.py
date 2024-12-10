from config import settings

class Endpoints:
    GetUser = f"{settings.server_address}/user/get_user/"
    PostUser = f"{settings.server_address}/user/register"
    ShowUserThemes = f"{settings.server_address}/theme/show_user_themes/"
    PostTheme = f"{settings.server_address}/theme"
    DeleteTheme = f"{settings.server_address}/theme/"
    PostSurveillance = f"{settings.server_address}/surveillance"
    ShowUserSurveillances = f"{settings.server_address}/surveillance/show_user_surveillances/"
    DeleteSurveillance = f"{settings.server_address}/surveillance/"
    PostComplain = f"{settings.server_address}/complain"
    ShowUserComplains = f"{settings.server_address}/complain/show_user_complains_pretty/"
    DeleteComplain = f"{settings.server_address}/complain/"


