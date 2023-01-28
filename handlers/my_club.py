from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, KeyboardButtonColor, EMPTY_KEYBOARD

from config import api, state_dispenser, ADMIN_CHAT
from database.database import get_user, get_server_by_country, get_server, insert_user, update_user, update_server
from functions.vpn import new_key, del_key
from states import ChangedServerData, InstructionsData, ctx


my_club_labeler = BotLabeler()
my_club_labeler.vbml_ignore_case = True
my_club_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@my_club_labeler.private_message(text="/mc")
@my_club_labeler.private_message(payload={'cmd': 'club'})
async def my_club_handler(message: Message):
    user = get_user(message.peer_id)
    if not user:
        insert_user(message.peer_id)
        user = get_user(message.peer_id)
    sub = user.end_date
    s = user.server
    if s:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Токен клуба', {'club': 'token'}))
        keyboard.row()
        keyboard.add(Text('Сменить сервер', {'club': 'change'}))
        keyboard.row()
        keyboard.add(Text('Инструкция', {'club': 'instruction'}))

        server = user.flag + ' ' + user.server if user.server is not None else 'No server'
        date = sub.strftime('%Y/%m/%d')

        await message.answer(f"Ваш клуб активен до\n{date}\nСервер клуба - {server}", keyboard=keyboard)

    else:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Годовая подписка'), color=KeyboardButtonColor.POSITIVE)
        keyboard.row()
        keyboard.add(Text('Месячная подписка'), color=KeyboardButtonColor.PRIMARY)

        await message.answer('😔Пока у вас нет собственного клуба интернета\n\n👀Только посмотрите, что вы получите:\n\n👉🏻Доступ к запрещенным сайтам (Canva, Instagram)\n👉🏻Высокую скорость работы\n👉🏻Скрытие вашего местоположения\n👉🏻100% защиту ваших данных\n\n💡Выберите срок оформления:', keyboard=keyboard)


@my_club_labeler.private_message(text="Токен клуба")
@my_club_labeler.private_message(payload={'club': 'token'})
async def club_token(message: Message):
    user = get_user(message.peer_id)
    token = user.access
    await message.answer('Вставьте отправленный ниже токен')
    await message.answer(f'{token}')


@my_club_labeler.private_message(text="Сменить сервер")
@my_club_labeler.private_message(payload={'club': 'change'})
async def change(message: Message):
    keyboard = Keyboard()
    servers = get_server(is_open=True)
    countries = []
    user = get_user(message.peer_id)
    if not servers:
        await message.answer('No servers available')
    for i in servers:
        if i.name not in countries and i.name != user.server:
            countries.append(i.name)
            keyboard.add(Text(f'{i.flag} {i.name} - {i.slots} слотов', {'change': 'server'}))
    
    await message.answer('Выберите сервер', keyboard=keyboard)


@my_club_labeler.private_message(payload={'change': 'server'})
async def change_server(message: Message):
    ctx.set(message.peer_id, {})
    await state_dispenser.set(message.peer_id, ChangedServerData.SERVER)

    flag = message.text.split(' - ')[0]
    country = flag.split(' ')

    data = ctx.get(message.peer_id)
    data['server'] = country[1]
    data['flag'] = flag
    ctx.set(message.peer_id, data)

    keyboard = Keyboard()
    keyboard.add(Text('Новый токен'))

    await message.answer('Вы успешно перевелись', keyboard=keyboard)


@my_club_labeler.private_message(state=ChangedServerData.SERVER)
async def new_token(message: Message):
    if message.text == 'Новый токен':
        data = ctx.get(message.peer_id)
        country = data['server']
        server = get_server_by_country(country)
        url = server.token
        key = new_key(url)
        user = get_user(message.peer_id)
        old_server = get_server(user.url)[0]

        if user.url is not None:
            del_key(user.url, user.token)
            update_server(user.url, old_server.name, old_server.flag, old_server.slots+1)
        
        update_user(message.peer_id, server.name, server.flag, url, key[0], key[1], user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, user.end_date)
        update_server(url, server.name, server.flag, server.slots-1)

        await message.answer('Вставьте отправленный ниже токен', keyboard=EMPTY_KEYBOARD)
        await message.answer(f'{key[1]}')

        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})
    else:
        keyboard = Keyboard()
        keyboard.add(Text('Новый токен'))
        
        await message.answer('Не верный ввод! Пожалуйста смените токен', keyboard=keyboard)


@my_club_labeler.private_message(text="Инструкция")
@my_club_labeler.private_message(payload={'club': 'instruction'})
async def instructions(message: Message):
    ctx.set(message.peer_id, {})
    await state_dispenser.set(message.peer_id, InstructionsData.PLATFORM)

    platforms = ['Android', 'IOS', 'Windows', 'Mac']

    keyboard = Keyboard(inline=True)
    
    for i in platforms:
        keyboard.add(Text(i))
        if i == 'IOS':
            keyboard.row()
        
    await message.answer('Now you have to choose your platform', keyboard=keyboard)