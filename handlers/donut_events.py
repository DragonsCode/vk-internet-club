from vkbottle.bot import BotLabeler, rules
from vkbottle import GroupEventType, GroupTypes

from config import api, ADMIN_CHAT
from database.database import get_user, update_user, insert_user
from handlers.admin import give_sub 

donut_labeler = BotLabeler()
donut_labeler.vbml_ignore_case = True
donut_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_CREATE, dataclass=GroupTypes.DonutSubscriptionCreate) # хэндлер для новых подписок
async def new_donut_sub(event: GroupTypes.DonutSubscriptionCreate):
    user_id = event.object.user_id # айди того кто оформил новую подписку integer
    amount = event.object.amount # сколько было оплачено в рублях integer
    amount_without_fee = event.object.amount_without_fee # сколько было оплачено без учета комиссии float

    if amount == 200:
        bot_user = await api.users.get(user_id)
        text = f'[id{user_id}|{bot_user[0].first_name} {bot_user[0].last_name}] оплатил подписку Donut'

        user = get_user(user_id)
        if not user:
            insert_user(user_id)
        else:
            if user.referal:
                ref = get_user(user.referal)
                if ref:
                    s = amount//10
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
                    bot_user = await api.users.get(ref.user_id)
                    text += f'\nИ его реферер [id{ref.user_id}|{bot_user[0].first_name} {bot_user[0].last_name}] получил 10% от этого платежа ({s}₽)'


        await give_sub(user_id, 30, text, 'Ваша оплата была принята')


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_PROLONGED, dataclass=dict)
async def donut_prol(event: GroupTypes.DonutSubscriptionProlonged):
    print("EVENT PROLONGED: ", event)
    print("EVENT PROLONGED OBJECT: ", event['object'])
    object = event['object']
    user_id = object['user_id']
    amount = object['amount']
    amount_without_fee = object['amount_without_fee']

    if amount == 200:
        bot_user = await api.users.get(user_id)
        text = f'[id{user_id}|{bot_user[0].first_name} {bot_user[0].last_name}] продлил подписку Donut'
        
        user = get_user(user_id)
        if not user:
            insert_user(user_id)
        else:
            if user.referal:
                ref = get_user(user.referal)
                if ref:
                    s = amount//10
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
                    bot_user = await api.users.get(ref.user_id)
                    text += f'\nИ его реферер [id{ref.user_id}|{bot_user[0].first_name} {bot_user[0].last_name}] получил 10% от этого платежа ({s}₽)'

        await give_sub(user_id, 30, text, 'Ваша оплата была принята')


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_CANCELLED, dataclass=GroupTypes.DonutSubscriptionCancelled)
async def donut_cancl(event: GroupTypes.DonutSubscriptionCancelled):
    user_id = event.object.user_id
    bot_user = await api.users.get(user_id)


    await api.messages.send(
        peer_id=user_id,
        message='Вы отменили подписку Donut',
        random_id=0
    )

    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=f'[id{user_id}|{bot_user[0].first_name} {bot_user[0].last_name}] отменил подписку Donut',
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

    bot_user = await api.users.get(user_id)
    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=f'У [id{user_id}|{bot_user[0].first_name} {bot_user[0].last_name}] истекла подписка Donut',
        random_id=0
    )