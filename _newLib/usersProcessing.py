import discord
import asyncio
import _dialog
from botdb.services import UserService
from botdb.entities.User import User

# Даёт роль на указанное кол-во секунд
async def give_timer_role(user, role: discord.Role, timeSeconds: int):

    await user.add_roles(role)
    await _dialog.message.log(message='{0} получил роль {1}'.format(user, role), color='yellow')
    await asyncio.sleep(timeSeconds)
    await _dialog.message.log(message='у {0} удалена роль {1}'.format(user, role), color='yellow')
    await user.remove_roles(role)


async def fix_level_role(user, rolesList, levelRoleDict, funcX, exp: float):
    level = funcX(exp)
    roleLevel = 0


    for levelKey in levelRoleDict.keys():
        if levelKey <= level and roleLevel < levelKey:
            roleLevel = levelKey

    print(f'fixLevelRole: level: {level}   roleLevel: {roleLevel}')

    for levelKey in levelRoleDict.keys():
        answer = discord.utils.get(user.roles, id=levelRoleDict[levelKey])

        if answer is not None:
            await user.remove_roles(answer)

    # На случай если roleLevel = 0, а роли на нулевом уровне нет
    if roleLevel in levelRoleDict.keys():
        await user.add_roles(discord.utils.get(rolesList, id=levelRoleDict[roleLevel]))


# Проверяет уровень и рольи пользователя
async def check_level_and_role(discordUser, discordGuild, levelRoleDict, funcX, checkAllRoles: bool = False):
    updated = False
    # Получение пользователя из БД
    try:
        DBUser = UserService.get_user_by_id(userId=discordUser.id)
    except ValueError:
        UserService.add_new_user(userId=discordUser.id)
        await _dialog.message.log(message=f'[{discordGuild.name}] Обнаружен пользователь {discordUser.name} ',
                                  color='yellow')
        DBUser = UserService.get_user_by_id(userId=discordUser.id)

    # Сверка уровня
    oldLevel = DBUser.level
    DBUser.level = funcX(exp=DBUser.exp)
    newLevel = DBUser.level
    if oldLevel != newLevel:
        UserService.update_user(user=DBUser)
        updated = True

    if not updated and not checkAllRoles and newLevel not in levelRoleDict:
        return updated


    # Получение роли, соответсвующей уровню
    roleLevel = 0
    for levelKey in levelRoleDict.keys():
        if levelKey <= newLevel:
            roleLevel = levelKey
        else:
            break

    # Поиск и удаление предыдущей роли за уровни
    if not checkAllRoles:
        newRoleIndex = levelRoleDict.keys().index(roleLevel)

        if newRoleIndex > 0:
            oldRoleIndex = levelRoleDict.keys().index(newRoleIndex - 1)
            answer = discord.utils.get(discordUser.roles, id=levelRoleDict[oldRoleIndex])

            if answer is not None:
                await discordUser.remove_roles(answer)
    # Удаление всех возможных ролей за уровни
    else:
        for levelKey in levelRoleDict.keys():
            answer = discord.utils.get(discordUser.roles, id=levelRoleDict[levelKey])

            if answer is not None:
                await discordUser.remove_roles(answer)

    if roleLevel in levelRoleDict.keys():
        await discordUser.add_roles(discord.utils.get(discordGuild.roles, id=levelRoleDict[roleLevel]))
