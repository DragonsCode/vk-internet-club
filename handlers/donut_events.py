from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, GroupEventType, GroupTypes

from config import api, state_dispenser, ADMIN_CHAT
from states import ctx, InstructionsData
from database.database import get_user, update_user, get_server

donut_labeler = BotLabeler()
donut_labeler.vbml_ignore_case = True
donut_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_CREATE, dataclass=GroupTypes.DonutSubscriptionCreate) # хэндлер для новых подписок
async def new_donut_sub(event: GroupTypes.DonutSubscriptionCreate):
    user_id = event.object.user_id # айди того кто оформил новую подпискуinteger
    amount = event.object.amount # сколько было оплачено в рублях integer
    amount_without_fee = event.object.amount_without_fee # сколько было оплачено без учета комиссии float

    # peer id и user id у пользователей одинаковый

    user = get_user(user_id)
    end_date = datetime.now() + timedelta(days=365)
    is_new = 1
    if user.end_date is not None:
        if user.end_date > datetime.now():
            is_new = 0
            end_date = user.end_date + timedelta(days=30)
    update_user(id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, end_date)

    if is_new:
        ctx.set(user_id, {})
        await state_dispenser.set(user_id, InstructionsData.SERVER)

        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Connect'))
        
        await api.messages.send(
            peer_id=int(user_id),
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

    # Отправка сообщения админ чату
    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=f'[id{user_id}|Пользователь] оплатил {amount}rub',
        random_id=0
    )


@donut_labeler.raw_event(GroupEventType.DONUT_SUBSCRIPTION_PROLONGED, dataclass=GroupTypes.DonutSubscriptionProlonged)
async def donut_prol(event: GroupTypes.DonutSubscriptionProlonged):
    user_id = event.object.user_id
    amount = event.object.amount
    amount_without_fee = event.object.amount_without_fee


    user = get_user(user_id)
    end_date = datetime.now() + timedelta(days=365)
    is_new = 1
    if user.end_date is not None:
        if user.end_date > datetime.now():
            is_new = 0
            end_date = user.end_date + timedelta(days=30)
    update_user(id, user.server, user.flag, user.url, user.token, user.access, user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, end_date)

    if is_new:
        ctx.set(user_id, {})
        await state_dispenser.set(user_id, InstructionsData.SERVER)

        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Connect'))
        
        await api.messages.send(
            peer_id=int(user_id),
            message='Received your payment, lets create your club!',
            keyboard=keyboard,
            random_id=0
        )
    else:
        await api.messages.send(
            peer_id=user_id,
            message='Вы продлили',
            random_id=0
        )

    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=f'[id{user_id}|Пользователь] продлил подписку',
        random_id=0
    )


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