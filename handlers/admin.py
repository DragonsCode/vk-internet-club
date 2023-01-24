from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, GroupEventType, GroupTypes

from config import api, state_dispenser, ADMIN_CHAT


admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=True)]


@admin_labeler.chat_message(text=['ok <id>', 'ok'], peer_ids=ADMIN_CHAT)
async def check_year_yes(message: Message, id=None):
    if id is None or not id.isdigit():
        await message.answer('Где айди?')
    else:
        await message.answer(f'[id{id}|Пользователь] принят')
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