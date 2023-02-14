from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text

from config import api, state_dispenser, ADMIN_CHAT
from states import ctx, InstructionsData
from database.database import insert_server, get_user, update_user, insert_user, update_server, get_server, delete_request, get_request
from functions.vpn import del_key


admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=True)]


async def give_sub(user_id, days, msg_adm, msg_usr):
    user = get_user(user_id)

    if not user:
        insert_user(user_id)
        user = get_user(user_id)

    ended = datetime.now() + timedelta(days=days)
    is_new = 1

    if user.end_date is not None:
        if user.end_date > datetime.now():
            is_new = 0
            ended = user.end_date + timedelta(days=days)
        else:
            pass
    else:
        pass
    update_user(user_id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, ended)

    if is_new:
        ctx.set(user_id, {})
        await state_dispenser.set(user_id, InstructionsData.SERVER)

        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Подключиться!'))
        
        await api.messages.send(
            peer_id=user_id,
            message='✅Отлично! Получил оплату\n\n📌Вы всего в паре шагов для подключения к нашему Клубу Интернета',
            keyboard=keyboard,
            random_id=0
        )
    
    else:
        await api.messages.send(
            peer_id=user_id,
            message=msg_usr,
            random_id=0
        )

    # Отправка сообщения админ чату
    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=msg_adm,
        random_id=0
    )


@admin_labeler.chat_message(text='[club211717723|@intervpn] Принять', peer_ids=ADMIN_CHAT)
# @admin_labeler.chat_message(payload={'ok': 'yes'})
async def check_year_yes(message: Message):
    payload = message.get_payload_json()

    if payload is None:
        await message.answer('Где айди?')
    else:
        id = int(payload['user_id'])
        msgid = int(payload['id'])
        msg = get_request(msgid)
        user = get_user(id)
        bot_user = await api.users.get(id)
        text = f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] получил подписку на 365 дней'

        if not msg:
            await message.answer('Данный запрос, кто-то уже отработал')
            return

        if not user:
            await message.answer(f'No user with id {id}')
        else:
            if user.referal:
                ref = get_user(user.referal)
                if ref:
                    s = 2000//10
                    update_user(
                        ref.user_id,
                        ref.server,
                        ref.flag,
                        ref.url,
                        ref.token,
                        ref.access,
                        ref.refs,
                        ref.ref_balance + s,
                        ref.referal,
                        ref.balance,
                        ref.is_admin,
                        ref.end_date
                    )
                    bot_ref = await api.users.get(ref.user_id)
                    text += f'\nИ его реферер [id{ref.user_id}|{bot_ref[0].first_name} {bot_ref[0].last_name}] получил 10% от этого платежа ({s}₽)'

        await give_sub(id, 365, text, 'Ваша оплата была принята')

        await api.messages.edit(peer_id=ADMIN_CHAT, message=f'Тут был запрос от [id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] на получение подписки на 365 дней, кто-то из администраторов ответил положительно', conversation_message_id=msg.msg_id)
        delete_request(msg.id)


@admin_labeler.chat_message(text='[club211717723|@intervpn] Отклонить', peer_ids=ADMIN_CHAT)
# @admin_labeler.chat_message(payload={'ok': 'no'})
async def check_year_no(message: Message):
    payload = message.get_payload_json()
    if payload is None:
        await message.answer('Где айди?')
    else:
        id = payload['user_id']
        msgid = int(payload['id'])
        msg = get_request(msgid)
        bot_user = await api.users.get(id)

        if not msg:
            await message.answer('Данный запрос, кто-то уже отработал')
            return

        await message.answer(f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] не принят')
        await api.messages.send(
            peer_id=int(id),
            message='Ваша оплата была отклонена',
            random_id=0
        )

        await api.messages.edit(peer_id=ADMIN_CHAT, message=f'Тут был запрос от [id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] на получение подписки на 365 дней, кто-то из администраторов ответил отрицательно', conversation_message_id=msg.msg_id)
        delete_request(msg.id)


@admin_labeler.chat_message(text=['/addserver <name> <flag> <token> <num>', '/addserver'], peer_ids=ADMIN_CHAT)
async def addserver(message: Message, name=None, flag=None, token=None, num=None):
    if flag is None or token is None or num is None:
        await message.answer('Пожалуйста указывайте аргументы правильно: /addserver <страна> <флаг> <токен> <количество слотов>\nКоличество слотов должно быть больше 0')
    else:
        if num.isdigit():
            if int(num) >= 1:
                insert_server(name, flag, token, num)
                await message.answer('Сервер добавлен успешно!')
            else:
                await message.answer('Количество слотов должно быть больше 0')
        else:
            await message.answer('Вы не врно указали количество слотов, укажите правильно этот аргумент как число большее 0')


@admin_labeler.chat_message(text=['/sub <num> <date> <link>', '/sub'], peer_ids=ADMIN_CHAT)
async def addsub(message: Message, num=None, date=None, link=None):
    if num is None or date is None or link is None:
        await message.answer('Пожалуйста указывайте аргументы правильно: /sub <количество> <время> <ссылка>\
            \nКоличество времени должно быть больше 0\
            \nВремя:\
            \ns - для лишения подписки\
            \nd - день\
            \nw - неделя\
            \nm - месяц\
            \ny - год')
    else:
        if num.isdigit():
            num = int(num)

            if num >= 1 and date in ['s', 'd', 'w', 'm', 'y']:
                get_link = link.split('vk.com/')[1]
                link = get_link[2:] if get_link[:2] == 'id' and get_link[2:].isdigit() else get_link
                users = await api.users.get(link)
                id = users[0].id
                user = get_user(id)
                bot_user = await api.users.get(id)

                if not user:
                    await message.answer(f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] не обнаружен в базе данных бота')
                    return

                if date == 's':
                    sub = user.end_date
                    s = None
                    if sub is not None:
                        s = user.end_date > datetime.now()
                    
                    if s:

                        if user.url is not None:
                            old_server = get_server(user.url)[0]
                            del_key(user.url, user.token)
                            update_server(user.url, old_server.name, old_server.flag, old_server.slots+1)

                        update_user(user.user_id, None, None, None, None, None, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, datetime(1, 1, 1))
                        await message.answer(f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] лишился подписки')
                        await api.messages.send(
                            peer_id=id,
                            message='Администратор лишил вас подписки!',
                            random_id=0
                        )
                    else:
                        await message.answer(f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] и без этого плачет без подписки. Пожалейте его!')
                    return
                
                days = num if date == 'd' else num * 7 if date == 'w' else num * 30 if date == 'm' else num * 365 if date == 'y' else num
                await give_sub(id, days, f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] получил подписку на {days} дней', f'Вам была выдана подписка на {days} дней')

            else:
                await message.answer('Количество должно быть больше 0')
        else:
            await message.answer('Вы не врно указали количество, укажите правильно аргумент количества как число большее 0')


@admin_labeler.chat_message(text='[club211717723|@intervpn] ✅Вывести', peer_ids=ADMIN_CHAT)
async def withdraw_yes(message: Message):
    payload = message.get_payload_json()
    if payload is None:
        await message.answer('Где айди?')
    else:
        id = int(payload['user_id'])
        amount = int(payload['amount'])
        msgid = int(payload['id'])
        msg = get_request(msgid)
        user = get_user(id)
        bot_user = await api.users.get(id)

        if not msg:
            await message.answer('Данный запрос, кто-то уже отработал')
            return

        update_user(id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance+amount, user.is_admin, user.end_date)
        
        await message.answer(f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] получил {amount}₽')
        await api.messages.send(
            peer_id=id,
            message=f'✅Мы отправили вам {amount}₽ выплаты по партнёрской программе\n\n❤️Спасибо за сотрудничество',
            random_id=0
        )

        await api.messages.edit(peer_id=ADMIN_CHAT, message=f'Тут был запрос от [id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] на получение вывода средств, кто-то из администраторов ответил положительно', conversation_message_id=msg.msg_id)
        delete_request(msg.id)

# [club211717723|@intervpn] [club188552039|@club188552039]
@admin_labeler.chat_message(text='[club211717723|@intervpn] ❌Отменить', peer_ids=ADMIN_CHAT)
async def withdraw_yes(message: Message):
    payload = message.get_payload_json()
    if payload is None:
        await message.answer('Где айди?')
    else:
        id = int(payload['user_id'])
        amount = int(payload['amount'])
        msgid = int(payload['id'])
        msg = get_request(msgid)
        user = get_user(id)
        bot_user = await api.users.get(id)

        if not msg:
            await message.answer('Данный запрос, кто-то уже отработал')
            return

        update_user(id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance+amount, user.referal, user.balance, user.is_admin, user.end_date)
        
        await message.answer(f'[id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] не получил вывод средств')
        await api.messages.send(
            peer_id=id,
            message=f'❌Мы отклонили вашу заявку на вывод {amount}₽\n\n💬Свяжитесь с [club202332903|технической поддержкой]',
            random_id=0
        )

        await api.messages.edit(peer_id=ADMIN_CHAT, message=f'Тут был запрос от [id{id}|{bot_user[0].first_name} {bot_user[0].last_name}] на получение вывода средств, кто-то из администраторов ответил отрицательно', conversation_message_id=msg.msg_id)
        delete_request(msg.id)