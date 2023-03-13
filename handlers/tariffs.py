from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink

from config import api, ADMIN_CHAT
from database.database import get_user, insert_request, update_request


tariffs_labeler = BotLabeler()
tariffs_labeler.vbml_ignore_case = True
tariffs_labeler.auto_rules = [rules.PeerRule(from_chat=False)]



@tariffs_labeler.private_message(text='Годовая подписка')
async def button_year(message: Message):
    keyboard = Keyboard(inline=True)
    keyboard.add(Text('Оплатить', {'pay': 'year'}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('Назад', {'cmd': 'club'}), color=KeyboardButtonColor.NEGATIVE)
    
    await message.answer('👀Клуб интернета на год стоит 1200₽\n🔥Скидка более 30%\n\n💡Для оплаты, используйте кнопку. Сразу после этого вы сможете воспользоваться любимым сервисом!', keyboard=keyboard)


@tariffs_labeler.private_message(text='Месячная подписка')
async def button_month(message: Message):
    keyboard = Keyboard(inline=True)
    keyboard.add(OpenLink('https://vk.com/intervpn?source=description&w=donut_payment-211717723', 'Оплатить'), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('Назад', {'cmd': 'club'}), color=KeyboardButtonColor.NEGATIVE)
    
    await message.answer('👀Клуб интернета на один месяц стоит всего 200₽\n\n💡Для оплаты, используйте кнопку. Сразу после этого вы сможете воспользоваться любимым сервисом!', keyboard=keyboard)



@tariffs_labeler.private_message(text='Оплатить')
@tariffs_labeler.private_message(payload={'pay': 'year'})
async def pay_year(message: Message):
    keyboard = Keyboard(inline=True)
    keyboard.add(Text('Я оплатил', {'year': 'yes'}))

    await message.answer('💎 Оплатить подписку на год можно переводом на карту!\n\nПереведите 1200₽ на карту, реквизиты которой отправлены следующим сообщением.\n\nПосле оплаты нажмите на кнопку «Я оплатил».', keyboard=keyboard)
    await message.answer('5469 1200 1001 6268')


# @tariffs_labeler.private_message(text='Я оплатил')
@tariffs_labeler.private_message(payload={'year': 'yes'})
async def year_yes(message: Message):
    user = await api.users.get(message.from_id)

    id = insert_request(0)

    keyboard = Keyboard(inline=True)
    keyboard.add(Text('Принять', {'user_id': message.peer_id, 'id': id.id}), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text('Отклонить', {'user_id': message.peer_id, 'id': id.id}), color=KeyboardButtonColor.NEGATIVE)

    msg = await api.messages.send(
        peer_ids=ADMIN_CHAT,
        message=f'[id{message.peer_id}|{user[0].first_name} {user[0].last_name}] оплатил на год',
        keyboard=keyboard,
        random_id=0
    )

    update_request(id.id, msg[0].conversation_message_id)

    await message.answer('Принято!\nПодождите пока администраторы проверят и одобрят вашу оплату!')

@tariffs_labeler.private_message(text='Оплатить')
@tariffs_labeler.private_message(payload={'pay': 'month'})
async def pay_month(message: Message):
    await message.answer('TEST: Вы оплатили на месяц')
    
    user = get_user(message.peer_id)
    sub = user.end_date
    if sub:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Токен клуба', {'club': 'token'}))
        keyboard.row()
        keyboard.add(Text('Сменить сервер', {'club': 'change'}))
        keyboard.row()
        keyboard.add(Text('Инструкция', {'club': 'instruction'}))

        await message.answer("Ваш клуб активен до\n\nСервер клуба - ", keyboard=keyboard)
        
    else:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Годовая подписка'), color=KeyboardButtonColor.POSITIVE)
        keyboard.row()
        keyboard.add(Text('Месячная подписка'), color=KeyboardButtonColor.PRIMARY)

        await message.answer('😔Пока у вас нет собственного клуба интернета\n\n👀Только посмотрите, что вы получите:\n\n👉🏻Доступ к запрещенным сайтам (Canva, Instagram)\n👉🏻Высокую скорость работы\n👉🏻Скрытие вашего местоположения\n👉🏻100% защиту ваших данных\n\n💡Выберите срок оформления:', keyboard=keyboard)
