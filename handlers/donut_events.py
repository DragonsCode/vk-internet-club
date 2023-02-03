from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, rules
from vkbottle import Keyboard, Text, GroupEventType, GroupTypes

from config import api, state_dispenser, ADMIN_CHAT
from states import ctx, InstructionsData
from database.database import get_user, update_user
from handlers.admin import give_sub 

donut_labeler = BotLabeler()
donut_labeler.vbml_ignore_case = True
donut_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_CREATE, dataclass=GroupTypes.DonutSubscriptionCreate) # хэндлер для новых подписок
async def new_donut_sub(event: GroupTypes.DonutSubscriptionCreate):
    user_id = event.object.user_id # айди того кто оформил новую подпискуinteger
    amount = event.object.amount # сколько было оплачено в рублях integer
    amount_without_fee = event.object.amount_without_fee # сколько было оплачено без учета комиссии float

    await give_sub(user_id, 30, f'[id{user_id}|Пользователь] оплатил подписку Donut', 'Ваша оплата была принята')


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_PROLONGED, dataclass=GroupTypes.DonutSubscriptionProlonged)
async def donut_prol(event: GroupTypes.DonutSubscriptionProlonged):
    user_id = event.object.user_id
    amount = event.object.amount
    amount_without_fee = event.object.amount_without_fee


    await give_sub(user_id, 30, f'[id{user_id}|Пользователь] продлил подписку Donut', 'Ваша оплата была принята')


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_CANCELLED, dataclass=GroupTypes.DonutSubscriptionCancelled)
async def donut_cancl(event: GroupTypes.DonutSubscriptionCancelled):
    user_id = event.object.user_id


    await api.messages.send(
        peer_id=user_id,
        message='Вы отменили подписку Donut',
        random_id=0
    )

    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=f'[id{user_id}|Пользователь] отменил подписку Donut',
        random_id=0
    )


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_EXPIRED, dataclass=GroupTypes.DonutSubscriptionExpired)
async def donut_cancl(event: GroupTypes.DonutSubscriptionExpired):
    user_id = event.object.user_id


    await api.messages.send(
        peer_id=user_id,
        message='Ваша подписка Donut истекла',
        random_id=0
    )

    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=f'У [id{user_id}|пользователя] истекла подписка Donut',
        random_id=0
    )