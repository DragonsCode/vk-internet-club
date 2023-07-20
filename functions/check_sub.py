from datetime import datetime

from config import scheduler, api, ADMIN_CHAT
from functions.vpn import del_key
from database.database import get_all_users, get_server, update_user, update_server


async def sub_end():
    users = get_all_users()
    notify = []
    dons = await api.groups.get_members("211717723", filter="donut")
    dons_ids = [i.id for i in dons.items]
    for user in users:
        if user.end_date is None:
            update_user(user.user_id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, datetime(1, 1, 1))
        
        if user.end_date is not None and user.end_date <= datetime.now() and user.user_id not in dons_ids:
            notify.append(user.user_id)

            if user.server is not None:
                old_server = get_server(user.url)[0]
                del_key(user.url, user.token)
                update_server(user.url, old_server.name, old_server.flag, old_server.slots+1)

            update_user(user.user_id, None, None, None, None, None, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, datetime(1, 1, 1))

            await api.messages.send(peer_id=user.user_id, message='Ваша подписка закончилась', random_id=0)
    
    if notify:
        text = ''

        for i in notify:
            user = await api.users.get(i)
            text += f'[id{i}|{user[0].first_name} {user[0].last_name}], '
        
        text += 'потеряли свои подписки ;)'

        await api.messages.send(peer_id=ADMIN_CHAT, message=text, random_id=0)

def sub_end_schedule():
    scheduler.add_job(sub_end, 'interval', days=1)
