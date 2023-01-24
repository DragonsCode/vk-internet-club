from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, KeyboardButtonColor, EMPTY_KEYBOARD

from config import api, state_dispenser, ADMIN_CHAT
from states import ChangedServerData, ctx


my_club_labeler = BotLabeler()
my_club_labeler.vbml_ignore_case = True
my_club_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@my_club_labeler.private_message(text="/mc")
@my_club_labeler.private_message(payload={'cmd': 'club'})
async def my_club_handler(message: Message):
    sub = 1
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


@my_club_labeler.private_message(text="Токен клуба")
@my_club_labeler.private_message(payload={'club': 'token'})
async def club_token(message: Message):
    await message.answer('Вставьте отправленный ниже токен')
    await message.answer('Токен: token')


@my_club_labeler.private_message(text="Сменить сервер")
@my_club_labeler.private_message(payload={'club': 'change'})
async def change(message: Message):
    keyboard = Keyboard()
    #TODO: Get servers with free slots from db
    servers = [('flag', 'country', 'slots')]
    for i in servers:
        keyboard.add(Text(f'{i[0]}{i[1]} - {i[2]} слотов', {'change': 'server'}))
    
    await message.answer('Выберите сервер', keyboard=keyboard)


@my_club_labeler.private_message(payload={'change': 'server'})
async def change_server(message: Message):
    ctx.set(message.peer_id, {})
    await state_dispenser.set(message.peer_id, ChangedServerData.SERVER)

    country = message.text.split(' - ')[0][1:]

    data = ctx.get(message.peer_id)
    data['server'] = country
    ctx.set(message.peer_id, data)

    keyboard = Keyboard()
    keyboard.add(Text('Новый токен'))

    await message.answer('Вы успешно перевелись', keyboard=keyboard)


@my_club_labeler.private_message(state=ChangedServerData.SERVER)
async def new_token(message: Message):
    if message.text == 'Новый токен':
        data = ctx.get(message.peer_id)
        server = data['server']
        #TODO: Generate token
        await message.answer(f'{server}! Вставьте отправленный ниже токен', keyboard=EMPTY_KEYBOARD)
        await message.answer('Токен: token')

        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})
    else:
        keyboard = Keyboard()
        keyboard.add(Text('Новый токен'))
        
        await message.answer('Не верный ввод! Пожалуйста смените токен', keyboard=keyboard)


@my_club_labeler.private_message(text="Инструкция")
@my_club_labeler.private_message(payload={'club': 'instruction'})
async def instructions(message: Message):
    await message.answer('Instructions')