from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink

from config import api, ADMIN_CHAT
from database.database import get_user, update_user, insert_request, update_request


ref_labeler = BotLabeler()
ref_labeler.vbml_ignore_case = True
ref_labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@ref_labeler.private_message(text="👨‍💼Партнерка")
@ref_labeler.private_message(payload={'ref': 'menu'})
async def ref_menu(message: Message):
    user = get_user(message.peer_id)

    keyboard = Keyboard(inline=True)
    keyboard.add(Text('💸Вывести средства', {'ref': 'withdraw'}))

    await message.answer(
        f'👥Вы пригласили: {user.refs} пользователей\n\n💹Вы заработали: {user.balance}₽\
        \n\n💰Партнёрский баланс: {user.ref_balance}₽\
        \n\n💫Ваша партнёрская ссылка: vk.me/intervpn?ref={message.peer_id}',
        keyboard=keyboard
        )


@ref_labeler.private_message(text="💸Вывести средства")
@ref_labeler.private_message(payload={'ref': 'withdraw'})
async def ref_withdraw(message: Message):
    user = get_user(message.peer_id)

    if user.ref_balance > 99:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Да', {'ref': 'yes'}))
        keyboard.add(Text('Нет', {'ref': 'menu'}))

        await message.answer(
            f'⭐️Вы можете вывести {user.ref_balance}₽\
            \n\n📝На данный момент – доступен вывод только на VK Pay\
            \n\n⭐️Выводим {user.ref_balance}₽ на [id{message.peer_id}|эту] страницу.\
            \n\n✅Выводим?',
            keyboard=keyboard
        )
    else:
        await message.answer('❌Выводить можно не менее 100₽')


@ref_labeler.private_message(payload={'ref': 'yes'})
async def ref_yes(message: Message):
    user = get_user(message.peer_id)
    bot_user = await api.users.get(message.from_id)

    update_user(message.peer_id, user.server, user.flag, user.url, user.token, user.access, user.refs, 0, user.referal, user.balance, user.is_admin, user.end_date)
    id = insert_request(0)

    keyboard = Keyboard(inline=True)
    keyboard = Keyboard(inline=True)
    keyboard.add(Text('✅Вывести', {'user_id': message.peer_id, 'amount': user.ref_balance, 'id': id.id}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('❌Отменить', {'user_id': message.peer_id, 'amount': user.ref_balance, 'id': id.id}), color=KeyboardButtonColor.NEGATIVE)

    msg = await api.messages.send(peer_ids=ADMIN_CHAT, message=f'💸[id{message.peer_id}|{bot_user[0].first_name} {bot_user[0].last_name}] запросил на вывод {user.ref_balance}₽ по партнёрской программе\n\n☝️Вывести на VK Pay', keyboard=keyboard, random_id=0)

    update_request(id.id, msg[0].conversation_message_id)

    keyboard1 = Keyboard()
    keyboard1.add(Text('🔮Мой клуб', {'cmd': 'club'}))
    keyboard1.row()
    keyboard1.add(Text("👨‍💼Партнерка"))
    keyboard1.row()
    keyboard1.add(OpenLink('https://vk.me/homa_nobi', '🆘Помощь'))

    await message.answer('💸Получили вашу заявку на вывод. Совсем скоро отправим средства\n\n☝️Ваша страница должна быть открытой, чтобы мы смогли написать сообщение и отправить выплату')

    await message.answer('🔺Главное меню. Для работы используйте кнопки ниже', keyboard=keyboard1)