
CREATE TABLE IF NOT EXISTS 'users' (
    'user_id' int NOT NULL PRIMARY KEY,
    'exp' real DEFAULT 0,
    'level' int DEFAULT 0,
    'messages_count' int DEFAULT 0,
    'symbols_count' int DEFAULT 0,
    'voice_chat_time' int DEFAULT 0,
    'volute_count' int DEFAULT 0,
    'exp_modifier' int DEFAULT 0);

=====

CREATE TABLE IF NOT EXISTS 'gif_groups' (
    'group_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'author_id' int REFERENCES users (user_id),
    'create_date' VARCHAR(10),
    'access_level' int DEFAULT 0,
    'group_type' VARCHAR(6) NOT NULL DEFAULT 'common',
    'name' VARCHAR(30) NOT NULL UNIQUE,
    'phrase' VARCHAR(100),

    CHECK (group_type IN('common', 'system', 'remove')));

=====

CREATE TABLE IF NOT EXISTS 'gifs' (
    'group_id' int REFERENCES gif_groups (group_id),
    'gif_url' VARCHAR(100) NOT NULL);

=====

CREATE TABLE IF NOT EXISTS 'guilds' (
    'guild_id' int NOT NULL PRIMARY KEY,
    'max_links' int DEFAULT 10,
    'mute_time' int DEFAULT 1200,
    'personal_roles_allowed' int DEFAULT 0,
    'ban_bot_functions' int,
    'no_links_role_id' int,
    'light_mute_role_id' int,
    'mute_role_id' int,
    'mute_voice_chat_role_id' int,
    'CHIELD_chat_id' int,
    'CHIELD_warning_count' int,
    'CHIELD_alert_count' int,
    'voice_chat_creator_id' int,
    'members_counter_chat_id' int,
    'roles_counter_chat_id' int,
    'welcome_phrase' VARCHAR(1500),
    'welcome_gif_group_id' int REFERENCES gif_groups (group_id)

    CHECK (personal_roles_allowed IN (0, 1)));

=====

CREATE TABLE IF NOT EXISTS 'guilds_members' (
    'user_id' int REFERENCES users (user_id),
    'guild_id' int REFERENCES guilds (guild_id),
    'visits_count' int DEFAULT 1,
    'warnings_count' int DEFAULT 0,
    'ban_bot_functions' int DEFAULT 0,
    'personal_role_id' int,
    'punishment_role_id' int,
    'punishment_end_date' VARCHAR(26),

    PRIMARY KEY (user_id, guild_id)
    CHECK (ban_bot_functions IN (0, 1)));

=====

CREATE TABLE IF NOT EXISTS 'level_roles' (
    'guild_id' int REFERENCES guilds (guild_id),
    'level' int NOT NULL,
    'role_id' int NOT NULL,

    PRIMARY KEY (guild_id, level));

=====

CREATE TABLE IF NOT EXISTS 'user_voice_chats' (
    'user_id' int UNIQUE REFERENCES users (user_id),
    'chat_name' VARCHAR(100) NOT NULL,
    'max_users_count' NOT NULL DEFAULT 100);

=====

CREATE TABLE IF NOT EXISTS 'questions' (
    'question_id'  INTEGER PRIMARY KEY AUTOINCREMENT,
    'author_user_id' int REFERENCES users (user_id),
    'uses_count' int NOT NULL DEFAULT 0,
    'question_text' VARCHAR(100) NOT NULL UNIQUE,
    'answer_text' VARCHAR(1850) NOT NULL);

=====

CREATE TABLE IF NOT EXISTS 'questions' (
    'question_id'  INTEGER PRIMARY KEY AUTOINCREMENT,
    'author_user_id' int REFERENCES users (user_id),
    'uses_count' int NOT NULL DEFAULT 0,
    'question_text' VARCHAR(100) NOT NULL UNIQUE,
    'answer_text' VARCHAR(1850) NOT NULL);

=====

CREATE TABLE IF NOT EXISTS 'general_settings' (
    'update_delay' int DEFAULT 60,
    'time_until_timeout' int DEFAULT 30,
    'timeouts_limit' int DEFAULT 5,
    'bomb_messages_time' int DEFAULT 15,
    'dialog_window_time' int DEFAULT 60);
