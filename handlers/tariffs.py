from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink

from config import api, state_dispenser, ADMIN_CHAT
from database.database import get_user


tariffs_labeler = BotLabeler()
tariffs_labeler.vbml_ignore_case = True
tariffs_labeler.auto_rules = [rules.PeerRule(from_chat=False)]



@tariffs_labeler.private_message(text='Годовая подписка')
async def button_year(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text('Оплатить', {'pay': 'year'}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('Назад', {'cmd': 'club'}), color=KeyboardButtonColor.NEGATIVE)
    
    await message.answer('👀Клуб интернета на год стоит 1 500₽\n🔥Скидка более 30%\n\n💡Для оплаты, используйте кнопку. Сразу после этого вы сможете воспользоваться любимым сервисом!', keyboard=keyboard)


@tariffs_labeler.private_message(text='Месячная подписка')
async def button_month(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(OpenLink('https://vk.com/donut/public218399445', 'Оплатить'), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('Назад', {'cmd': 'club'}), color=KeyboardButtonColor.NEGATIVE)
    
    await message.answer('👀Клуб интернета на один месяц стоит всего 200₽\n\n💡Для оплаты, используйте кнопку. Сразу после этого вы сможете воспользоваться любимым сервисом!', keyboard=keyboard)



@tariffs_labeler.private_message(text='Оплатить')
@tariffs_labeler.private_message(payload={'pay': 'year'})
async def pay_year(message: Message):
    await message.answer('Переведите по карте и администраторы выдадут вам подписку как только проверят')

    user = await api.users.get(message.from_id)

    await api.messages.send(
        peer_id=ADMIN_CHAT,
        message=f'[id{message.peer_id}|{user[0].first_name} {user[0].last_name}] оплатит на год\ntype "ok {message.peer_id}" to apply or "not ok {message.peer_id}" to discard',
        random_id=0
    )

@tariffs_labeler.private_message(text='Оплатить')
@tariffs_labeler.private_message(payload={'pay': 'month'})
async def pay_month(message: Message):
    await message.answer('Вы оплатили на месяц')
    
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
