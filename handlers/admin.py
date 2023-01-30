from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text

from config import api, state_dispenser, ADMIN_CHAT
from states import ctx, InstructionsData
from database.database import insert_server, get_user, update_user


admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=True)]


@admin_labeler.chat_message(text=['[club211717723|@intervpn] Принять <id>', '[club211717723|@intervpn] Принять'], peer_ids=ADMIN_CHAT)
# @admin_labeler.chat_message(payload={'ok': 'yes'})
async def check_year_yes(message: Message, id=None):
    payload = message.get_payload_json()
    if payload is None:
        await message.answer('Где айди?')
    else:
        id = payload['user_id']
        user = get_user(id)
        end_date = datetime.now() + timedelta(days=365)
        is_new = 1
        if user.end_date is not None:
            if user.end_date > datetime.now():
                is_new = 0
                end_date = user.end_date + timedelta(days=365)
        update_user(id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, end_date)

        user = await api.users.get(id)
        await message.answer(f'[id{id}|{user[0].first_name} {user[0].last_name}] принят')

        if is_new:
            ctx.set(int(id), {})
            await state_dispenser.set(int(id), InstructionsData.SERVER)

            keyboard = Keyboard(inline=True)
            keyboard.add(Text('Подключиться!'))
            
            await api.messages.send(
                peer_id=int(id),
                message='✅Отлично! Получил оплату\n\n📌Вы всего в паре шагов для подключения к нашему Клубу Интернета',
                keyboard=keyboard,
                random_id=0
            )
        else:
            await api.messages.send(
                peer_id=int(id),
                message='Ваша оплата была принята',
                random_id=0
            )


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