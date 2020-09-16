import discord
from generallib import mainlib, textfile
from mycommands import dilogcomm
from usersettings import params
from configs import config


# Устанавливает роль в списке Access_set
async def set_Access_role(bot, accessname: str, ctx: discord.ext.commands.Context):
    rolename = mainlib.get_rolename(ctx)
    if rolename is None:
        return
    params.accessparams[accessname] = rolename
    textfile.WriteParams(ParamsDict=params.accessparams, filename=config.params['user_settings'])
    await dilogcomm.printlog(bot=bot, author=ctx.author, message='плашка-{0} изменена на \"{1}\"'.format(accessname, rolename))
