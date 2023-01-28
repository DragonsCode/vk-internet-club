from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, GroupEventType, GroupTypes

from config import api, state_dispenser, ADMIN_CHAT
from states import ctx, InstructionsData
from database.database import insert_server, get_user, update_user


admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=True)]


@admin_labeler.chat_message(text=['ok <id>', 'ok'], peer_ids=ADMIN_CHAT)
async def check_year_yes(message: Message, id=None):
    if id is None or not id.isdigit():
        await message.answer('Где айди?')
    else:
        user = get_user(id)
        end_date = datetime.now()# + timedelta(days=365)
        is_new = 1
        if user.end_date is not None:
            if user.end_date > datetime.now():
                is_new = 0
                end_date = user.end_date# + timedelta(days=365)
        update_user(id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, end_date)

        await message.answer(f'[id{id}|Пользователь] принят')

        if is_new:
            ctx.set(int(id), {})
            await state_dispenser.set(int(id), InstructionsData.SERVER)

            keyboard = Keyboard(inline=True)
            keyboard.add(Text('Connect'))
            
            await api.messages.send(
                peer_id=int(id),
                message='Received your payment, lets create your club!',
                keyboard=keyboard,
                random_id=0
            )
        else:
            await api.messages.send(
                peer_id=int(id),
                message='Ваша оплата была принята',
                random_id=0
            )


@admin_labeler.chat_message(text=['not ok <id>', 'not ok'], peer_ids=ADMIN_CHAT)
async def check_year_no(message: Message, id=None):
    if id is None or not id.isdigit():
        await message.answer('Где айди?')
    else:
        await message.answer(f'[id{id}|Пользователь] не принят')
        await api.messages.send(
            peer_id=int(id),
            message='Ваша оплата была отклонена',
            random_id=0
        )


@admin_labeler.chat_message(text=['/addserver <name> <flag> <token> <num>', '/addserver'], peer_ids=ADMIN_CHAT)
async def addserver(message: Message, name=None, flag=None, token=None, num=None):
    if flag is None or token is None or num is None:
        await message.answer('please specify the arguments correctly: /addserver <name> <flag> <token> <number of slots>\nNote that number of slots should be greater than 0')
    else:
        if num.isdigit():
            if int(num) >= 1:
                insert_server(name, flag, token, num)
                await message.answer('Server added successfully!')
            else:
                await message.answer('number of slots should be greater than 0')
        else:
            await message.answer('you must specify number of slots as integer greater than 0')