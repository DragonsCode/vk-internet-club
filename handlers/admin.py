from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text

from config import api, state_dispenser, ADMIN_CHAT
from states import ctx, InstructionsData
from database.database import insert_server, get_user, update_user


admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=True)]


async def give_sub(user_id, days, msg_adm, msg_usr):
    user = get_user(user_id)
    end_date = datetime.now() + timedelta(days=days)
    is_new = 1
    if user.end_date is not None:
        if user.end_date > datetime.now():
            is_new = 0
            end_date = user.end_date + timedelta(days=days)
    update_user(user_id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, end_date)

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


@admin_labeler.chat_message(text=['[club211717723|@intervpn] Принять <id>', '[club211717723|@intervpn] Принять'], peer_ids=ADMIN_CHAT)
# @admin_labeler.chat_message(payload={'ok': 'yes'})
async def check_year_yes(message: Message, id=None):
    payload = message.get_payload_json()
    if payload is None:
        await message.answer('Где айди?')
    else:
        id = payload['user_id']
        await give_sub(id, 365, f'[id{id}|Пользователь] получил подписку на 365 дней', 'Ваша оплата была принята')


@admin_labeler.chat_message(text=['[club211717723|@intervpn] Отклонить <id>', '[club211717723|@intervpn] Отклонить'], peer_ids=ADMIN_CHAT)
# @admin_labeler.chat_message(payload={'ok': 'no'})
async def check_year_no(message: Message, id=None):
    payload = message.get_payload_json()
    if payload is None:
        await message.answer('Где айди?')
    else:
        id = payload['user_id']
        user = await api.users.get(id)
        await message.answer(f'[id{id}|{user[0].first_name} {user[0].last_name}] не принят')
        await api.messages.send(
            peer_id=int(id),
            message='Ваша оплата была отклонена',
            random_id=0
        )


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
        await message.answer('Пожалуйста указывайте аргументы правильно: !sub <количество> <время> <ссылка>\
            \nКоличество времени должно быть больше 0\
            \nВремя:\
            \ns - для лишения подписки (указывать количество 1)\
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

                if not user:
                    await message.answer(f'[id{id}|Пользователь] не обнаружен в базе данных бота')

                if date == 's':
                    update_user(user.user_id, None, None, None, None, None, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, datetime(1, 1, 1))
                    await message.answer(f'[id{id}|Пользователь] лишился подписки')
                    await api.messages.send(
                        peer_id=id,
                        message='Администратор лишил вас подписки!',
                        random_id=0
                    )
                    return
                
                days = num if date == 'd' else num * 7 if date == 'w' else num * 30 if date == 'm' else num * 365 if date == 'y' else num
                await give_sub(id, days, f'[id{id}|Пользователь] получил подписку на {days} дней', f'Вам была выдана подписка на {days} дней')

            else:
                await message.answer('Количество должно быть больше 0')
        else:
            await message.answer('Вы не врно указали количество, укажите правильно аргумент количества как число большее 0')