
# проверяет нилчие роли в списк по её названию
def is_exist(rolelist: list, serchrole: str):
    for curr_role in rolelist:
        if curr_role.name == serchrole:
            return True
    return False

# находит роль по её названию
def find_role(rolelist: list, serchrole: str):
    for curr_role in rolelist:
        if curr_role.name == serchrole:
            return curr_role
    return None
