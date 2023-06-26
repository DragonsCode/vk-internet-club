import sqlite3
from dataclasses import dataclass
import datetime

@dataclass
class User:
    user_id: int
    server: str
    flag: str
    url: str
    token: int
    access: str
    refs: int
    ref_balance: int
    referal: int
    balance: int
    is_admin: int
    end_date: datetime.datetime

@dataclass
class Server:
    name: str
    flag: str
    token: str
    slots: int

@dataclass
class Request:
    id: int
    msg_id: int



def create_tables():
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, server TEXT DEFAULT NULL, flag TEXT DEFAULT NULL, url TEXT DEFAULT NULL, token INTEGER DEFAULT NULL, access TEXT DEFAULT NULL, refs INT DEFAULT 0, ref_balance INT DEFAULT 0, referal INT DEFAULT 0, balance INT DEFAULT 0, is_admin INT DEFAULT 0, end_date TIMESTAMP DEFAULT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS servers(name TEXT, flag TEXT, token TEXT, slots INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS requests(id INTEGER PRIMARY KEY, msg_id INTEGER)")
    con.commit()
    cur.close()
    con.close()


def insert_request(msg_id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("INSERT INTO requests(msg_id) VALUES (?) RETURNING id, msg_id", (msg_id,))
    row = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    return Request(*row)


def update_request(id: int, msg_id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("UPDATE requests SET msg_id = ? WHERE id = ? RETURNING id, msg_id", (msg_id, id,))
    row = cur.fetchone()
    print('ROW IS:', row)
    con.commit()
    cur.close()
    con.close()
    return Request(*row)


def get_request(id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("SELECT * FROM requests WHERE id = ?", (id,))
    row = cur.fetchone()
    if not row:
        return False
    cur.close()
    con.close()
    return Request(*row)


def delete_request(id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("DELETE FROM requests WHERE id = ?", (id,))
    cur.close()
    con.close()


def insert_user(user_id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    check_db = cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    is_in_db = check_db.fetchall()
    if is_in_db:
        cur.close()
        con.close()
        return True
    sub = datetime.datetime(1, 1, 1)
    cur.execute("INSERT INTO users(user_id, end_date) VALUES (?, ?)", (user_id, sub))
    con.commit()
    cur.close()
    con.close()
    return False


def get_user(user_id: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    check_user = cur.execute("SELECT user_id, server, flag, url, token, access, refs, ref_balance, referal, balance, is_admin, end_date FROM users WHERE user_id = ?", (user_id,))
    user = check_user.fetchone()
    cur.close()
    con.close()
    if not user:
        return False
    return User(*user)

def get_referals(owner_id: int) -> list[User]:
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    check_user = cur.execute("SELECT user_id, server, flag, url, token, access, refs, ref_balance, referal, balance, is_admin, end_date FROM users WHERE referal = ?", (owner_id,))
    res = check_user.fetchall()
    cur.close()
    con.close()
    users = []
    for i in res:
        users.append(User(*i))
    return users

def get_all_users() -> list[User]:
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    check_user = cur.execute("SELECT user_id, server, flag, url, token, access, refs, ref_balance, referal, balance, is_admin, end_date FROM users")
    res = check_user.fetchall()
    cur.close()
    con.close()
    users = []
    for i in res:
        users.append(User(*i))
    return users


def update_user(user_id: int, server, flag, url, token, access, refs, ref_balance, referal, balance, is_admin, end_date):
    # some shitcode goes here
    # check_data = [
    # 'server = '+user_data.get('server', 0) if user_data.get('server', 0) else '',
    # 'token = '+user_data.get('token', 0) if user_data.get('token', 0) else '',
    # 'refs = '+user_data.get('refs', 0) if user_data.get('refs', 0) else '',
    # 'ref_balance = '+user_data.get('ref_balance', 0) if user_data.get('ref_balance', 0) else '',
    # 'referal = '+user_data.get('referal', 0) if user_data.get('referal', 0) else '',
    # 'balance = '+user_data.get('balance', 0) if user_data.get('balance', 0) else '',
    # 'is_admin = '+user_data.get('is_admin', 0) if user_data.get('is_admin', 0) else '',
    # 'end_date = '+user_data.get('end_date', 0) if user_data.get('end_date', 0) else ''
    # ]
    # lst_data = [x for x in check_data if x!='']
    # data = ', '.join(lst_data)

    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("UPDATE users SET server = ?, flag = ?, url = ?, token = ?, access = ?, refs = ?, ref_balance = ?, referal = ?, balance = ?, is_admin = ?, end_date = ? WHERE user_id = ?", (server, flag, url, token, access, refs, ref_balance, referal, balance, is_admin, end_date, user_id,))
    con.commit()
    cur.close()
    con.close()


def insert_server(name: str, flag: str, token: str, slots: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("INSERT INTO servers VALUES (?, ?, ?, ?)", (name, flag, token, slots,))
    con.commit()
    cur.close()
    con.close()


def get_server(token: str=None, is_open: bool=False) -> list[Server]:
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    res = None
    if token is None:
        if is_open:
            res = cur.execute("SELECT * FROM servers WHERE slots >= 1")
        else:
            res = cur.execute("SELECT * FROM servers")
    else:
        if is_open:
            res = cur.execute("SELECT * FROM servers WHERE token = ? AND slots >= 1", (token,))
        else:
            res = cur.execute("SELECT * FROM servers WHERE token = ?", (token,))
    response = res.fetchall()
    results = []
    con.commit()
    cur.close()
    con.close()
    for i in response:
        results.append(Server(*i))
    return results


def get_server_by_country(country: str):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM servers WHERE name = ? AND slots >= 1", (country,))
    response = res.fetchone()
    result = Server(*response)
    cur.close()
    con.close()
    return result


def update_server(token: str, name: str, flag: str, slots: int):
    con = sqlite3.connect('bot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("UPDATE servers SET name = ?, flag = ?, slots = ? WHERE token = ?", (name, flag, slots, token,))
    con.commit()
    cur.close()
    con.close()