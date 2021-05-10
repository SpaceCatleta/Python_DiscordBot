import random
import sqlite3
import discord
from generallib import textfile
import functions.gif_triggers_db_proc as TDB


# id автора, название, описание, доступ, gif
triggers_tree = []
triggers_db: TDB.GifTriggersDataBase


def init(path: str):
    global triggers_db
    triggers_db = TDB.GifTriggersDataBase(path)

def get_trigger_info(name: str):
    ans = triggers_db.get_trigger(name=name)
    if ans == -1:
        return -1
    else:
        count = len(triggers_db.get_group_gif(name=ans.name))
        return 'триггер:{0}   фраза:{1}\nавтор:{2}   доступ всем:{3}\nкол-во gif:{4}'.\
            format(ans.name, ans.discr, ans.author_id, 'yes' if ans.access else 'no', count)

def switch_lock(name: str):
    triggers_db.switch_lock(name=name)


def delete_trigger(name: str):
    triggers_db.delete_trigger(name=name)


def add_new_trigger(author_id, name: str, discr: str='None'):
    global triggers_db
    try:
        item = TDB.Gif_Trigger(name=name, discr=discr, author_id=author_id)
        triggers_db.add_new_trigger(item=item)
    except sqlite3.IntegrityError:
        return -1
    return 0


def add_new_gif(user_id, name: str, url: str, is_admin: bool=False):
    global triggers_db
    trigger: TDB.Gif_Trigger = triggers_db.get_trigger(name=name.lower())
    if trigger == None:
        return 'ключевое слово {0} не найдено'.format(name)
    elif not is_admin and user_id != trigger.author_id and not trigger.access:
        return 'отстствуют права для редактирования'

    triggers_db.add_gif(group_name=trigger.name, url=url)

    return 0


def update_trigger_discr(name: str, new_discr: str):
    return triggers_db.update_trigger_discr(name=name, new_discr=new_discr)


def get_trigger_list():
    triggers = triggers_db.get_triggers_list()
    return '\n'.join(['название - {0}; кол-во gif - {1}; доступ всем - {2}'.
                     format(trig.name, trig.count, 'yes' if trig.access  else 'no') for trig in triggers])


def get_random_gif(group_name: str):
    return random.choice(triggers_db.get_group_gif(name=group_name))[0]


def get_trigger(name: str):
    return triggers_db.get_trigger(name=name)




