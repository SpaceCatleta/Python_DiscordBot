from botdb.entities.UserVoiceChat import UserVoiceChat
from botdb.repository import UserVoiceChatRep as Repos


# ====ADD============================
# Создаёт новую запись. Требуемые поля: authorId и name
def add_new_user_voice_chat(userVoiceChat: UserVoiceChat):
    Repos.add_new_user_voice_chat(userVoiceChat=userVoiceChat)


# ====GET============================
def get_user_voice_chat_by_user_id(userId: int):
    row = Repos.get_user_voice_chat_by_user_id(userId=userId)
    if row is None:
        raise ValueError('UserVoiceChatService.get_user_voice_chat_by_user_id(): returned row is null')
    return UserVoiceChat(userId=row[0], chatName=row[1], maxUsersCount=row[2])

def get_all_user_voice_chats():
    rows = Repos.get_all_user_voice_chats()
    return [UserVoiceChat(userId=row[0], chatName=row[1], maxUsersCount=row[2]) for row in rows]


# ====UPDATE============================
def update_user_voice_chat_by_user_id(userVoiceChat: UserVoiceChat):
    Repos.update_user_voice_chat(userVoiceChat=userVoiceChat)


# ====DELETE============================
def delete_user_voice_chat_by_user_id(userId: int):
    Repos.delete_user_voice_chat_by_user_id(userId=userId)


def clear_table():
    Repos.clear_table()
