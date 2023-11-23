import sqlite3

database = sqlite3.connect("bot.sqlite")
cursor = database.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, surname TEXT, phone INTEGER, disease TEXT)')
database.commit()


def add_user(message):
    cursor.execute("SELECT id FROM users WHERE id=?", (message.chat.id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)", (message.chat.id, "name", "surname", "phone", "disease"))
        database.commit()
    else:
        return False


def drop_user_reg(user_id):
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    database.commit()


def add_user_name(message):
    cursor.execute("UPDATE users SET name=? WHERE id=?", (message.text, message.chat.id))
    database.commit()


def add_user_surname(message):
    cursor.execute("UPDATE users SET surname=? WHERE id=?", (message.text, message.chat.id))
    database.commit()


def add_user_phone(message):
    cursor.execute("UPDATE users SET phone=? WHERE id=?", (message.text, message.chat.id))
    database.commit()


def get_user_name(user_id):
    cursor.execute("SELECT name FROM users WHERE id=?", (user_id,))
    user_name = cursor.fetchone()[0]
    return user_name


def get_user_surname(user_id):
    cursor.execute("SELECT surname FROM users WHERE id=?", (user_id,))
    user_surname = cursor.fetchone()[0]
    return user_surname


def get_user_phone(user_id):
    cursor.execute("SELECT phone FROM users WHERE id=?", (user_id,))
    user_phone = cursor.fetchone()[0]
    return user_phone


def add_user_disease(chat_id, disease):
    cursor.execute("SELECT * FROM users WHERE id=?", (chat_id,))
    user_data = cursor.fetchone()

    if user_data:
        existing_diseases = user_data[4] if user_data[4] else ""
        new_diseases = f"{existing_diseases},{disease}" if existing_diseases else disease

        cursor.execute("UPDATE users SET disease=? WHERE id=?", (new_diseases, chat_id))
        database.commit()
        return True
    else:
        return False


def get_user_disease(user_id):
    cursor.execute("SELECT disease FROM users WHERE id=?", (user_id,))
    user_disease = cursor.fetchone()
    return user_disease[0] if user_disease else None


def drop_user_disease(chat_id):
    cursor.execute("UPDATE users SET disease=? WHERE id=?", ("", chat_id))
    database.commit()



