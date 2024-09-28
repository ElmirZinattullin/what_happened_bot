from dotenv import set_key, get_key, dotenv_values

settings_path = "settings.txt"
settings = dotenv_values(settings_path)
my = -4597396724


def set_support_chat_id(val:str):
    global SUPPORT_CHAT_ID
    set_key(settings_path, "SUPPORT_CHAT_ID", val)
    SUPPORT_CHAT_ID = val
    print(SUPPORT_CHAT_ID)

def get_support_chat_id():
    global SUPPORT_CHAT_ID
    if SUPPORT_CHAT_ID:
        return SUPPORT_CHAT_ID
    else:
        SUPPORT_CHAT_ID = get_key(settings_path, "SUPPORT_CHAT_ID")
    return SUPPORT_CHAT_ID

SUPPORT_CHAT_ID = None
get_support_chat_id()