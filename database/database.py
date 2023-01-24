import sqlite3



def create_tables():
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, server TEXT DEFAULT NULL, token TEXT DEFAULT NULL, refs INT DEFAULT 0, ref_balance INT DEFAULT 0, referal INT DEFAULT 0, balance INT DEFAULT 0, is_admin INT DEFAULT 0, end_date DATE DEFAULT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS servers(name TEXT, flag TEXT, token TEXT, slots INT)")
    cur.close()
    con.close()


def insert_user(user_id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    check_db = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    is_in_db = check_db.fetchall()
    if is_in_db:
        cur.close()
        con.close()
        return True
    cur.execute("INSERT INTO users(user_id) VALUES (?)", (user_id,))
    cur.close()
    con.close()
    return False


def get_user(user_id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    check_user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = check_user.fetchone()
    cur.close()
    con.close()
    if not user:
        return False
    return user


def update_user(user_id: int, user_data: dict):
    check_data = [
    'server = '+user_data.get('server', 0) if user_data.get('server', 0) else '',
    'token = '+user_data.get('token', 0) if user_data.get('token', 0) else '',
    'refs = '+user_data.get('refs', 0) if user_data.get('refs', 0) else '',
    'ref_balance = '+user_data.get('ref_balance', 0) if user_data.get('ref_balance', 0) else '',
    'referal = '+user_data.get('referal', 0) if user_data.get('referal', 0) else '',
    'balance = '+user_data.get('balance', 0) if user_data.get('balance', 0) else '',
    'is_admin = '+user_data.get('is_admin', 0) if user_data.get('is_admin', 0) else '',
    'end_date = '+user_data.get('end_date', 0) if user_data.get('end_date', 0) else ''
    ]

    lst_data = [x for x in check_data if x!='']

    data = ', '.join(lst_data)

    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute(f"UPDATE users SET {data} WHERE user_id = ?", (user_id,))
    cur.close()
    con.close()


def insert_server(name: str, flag: str, token: str, slots: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("INSERT INTO servers VALUES (?, ?, ?, ?)", (name, flag, token, slots,))
    cur.close()
    con.close()