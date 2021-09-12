import sqlite3 as sql
from botdb.entities.GeneralSettings import GeneralSettings

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def create_general_settings():
    cursor.execute(""" INSERT INTO general_settings DEFAULT VALUES; """)
    connection.commit()


# ====GET============================
def get_general_settings():
    cursor.execute(""" SELECT * from general_settings; """)
    return cursor.fetchone()


def get_general_settings_count():
    cursor.execute(""" SELECT COUNT(update_delay) FROM general_settings; """)
    return cursor.fetchone()


# ====UPDATE============================
def update_general_settings(generalSettings: GeneralSettings):
    cursor.execute("""
        UPDATE general_settings SET
        update_delay = :updateDelay,
        time_until_timeout = :timeUntilTimeout,
        timeouts_limit = :timeoutsLimit,
        bomb_messages_time = :bombMessagesTime,
        dialog_window_time = :dialogWindowTime
        """, generalSettings.__dict__)
    connection.commit()


# ====DELETE============================
def delete_general_settings():
    cursor.execute(""" DELETE FROM general_settings; """)
    connection.commit()
