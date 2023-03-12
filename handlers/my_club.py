from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, OpenLink, KeyboardButtonColor, EMPTY_KEYBOARD

from datetime import datetime

from config import state_dispenser, api
from database.database import get_user, get_server_by_country, get_server, insert_user, update_user, update_server
from functions.vpn import new_key, del_key
from states import ChangedServerData, InstructionsData, ctx


my_club_labeler = BotLabeler()
my_club_labeler.vbml_ignore_case = True
my_club_labeler.auto_rules = [rules.PeerRule(from_chat=False)]



@my_club_labeler.private_message(text="⚙Сменить сервер")
@my_club_labeler.private_message(payload={'club': 'change'})
async def change(message: Message):
    keyboard = Keyboard()
    servers = get_server(is_open=True)
    countries = []
    user = get_user(message.peer_id)

    if not servers:
            await message.answer('❌На данный момент нет свободных локаций')
            return

    k = len(servers) - 1
    if user.server is not None:
        countries.append(user.server)
        k -= 1

    for i in servers:
        if i.name not in countries and i.name != user.server:
            countries.append(i.name)
            keyboard.add(Text(f'{i.flag} {i.name} - {i.slots} слотов', {'change': 'server'}))
            if k > 0:
                keyboard.row()
                k -= 1

    if not countries:
            await message.answer('❌На данный момент нет свободных локаций')
            return
    
    await message.answer('❓Выберите сервер, на который желаете перевести ваш клуб интернета', keyboard=keyboard)


@my_club_labeler.private_message(text=["Мой клуб", "🔮Мой клуб"])
@my_club_labeler.private_message(payload={'cmd': 'club'})
async def my_club_handler(message: Message):
    user = get_user(message.peer_id)
    if not user:
        insert_user(message.peer_id)
        user = get_user(message.peer_id)
    sub = user.end_date
    s = None
    if sub is not None:
        s = user.end_date > datetime.now()
    if s:
        server = user.flag + ' ' + user.server if user.server is not None else False

        if not server:
            await change(message)
            return

        date = sub.strftime('%Y.%m.%d')

        keyboard = Keyboard(inline=True)
        keyboard.add(Text('📦Токен клуба', {'club': 'token'}))
        keyboard.row()
        keyboard.add(Text('⚙Сменить сервер', {'club': 'change'}))
        keyboard.row()
        keyboard.add(Text('📃Инструкция', {'club': 'instruction'}))
        keyboard.row()
        keyboard.add(OpenLink('https://vk.me/homa_nobi', '🆘Помощь'))

        await message.answer(f"✅Ваш клуб активен до «{date}»\n\n💻Сервер клуба - {server}", keyboard=keyboard)

    else:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Годовая подписка'), color=KeyboardButtonColor.POSITIVE)
        keyboard.row()
        keyboard.add(Text('Месячная подписка'), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(OpenLink('https://vk.me/homa_nobi', '🆘Помощь'))

        await message.answer('😔Пока у вас нет собственного клуба интернета\n\n👀Только посмотрите, что вы получите:\n\n👉🏻Доступ к запрещенным сайтам (Canva, Instagram)\n👉🏻Высокую скорость работы\n👉🏻Скрытие вашего местоположения\n👉🏻100% защиту ваших данных\n\n💡Выберите срок оформления:', keyboard=keyboard)


@my_club_labeler.private_message(text="📦Токен клуба")
@my_club_labeler.private_message(payload={'club': 'token'})
async def club_token(message: Message):
    keyboard = Keyboard(inline=True)
    keyboard.add(Text('📃Инструкция', {'club': 'instruction'}))
    user = get_user(message.peer_id)
    token = user.access
    await message.answer('✅Вставьте отправленный ниже токен в приложение Outline, и подключайтесь к вашему клубу интернета!', keyboard=keyboard)
    await message.answer(f'{token}')


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
    keyboard.add(Text('🚀Новый токен'))

    await message.answer(f'✅Вы успешно перевели свой клуб интернета в {flag}.\n\n💡Вы сменили локацию, поэтому изменился токен клуба\n\n💫Нажмите на кнопку, чтобы вернуть доступ', keyboard=keyboard)


@my_club_labeler.private_message(state=ChangedServerData.SERVER)
async def new_token(message: Message):
    if message.text == '🚀Новый токен':
        data = ctx.get(message.peer_id)
        country = data['server']
        server = get_server_by_country(country)
        url = server.token
        bot_user = await api.users.get(message.peer_id)
        user = get_user(message.peer_id)

        if user.url is not None:
            old_server = get_server(user.url)[0]
            del_key(user.url, user.token)
            update_server(user.url, old_server.name, old_server.flag, old_server.slots+1)
        
        key = new_key(url, f'{bot_user[0].first_name} {bot_user[0].last_name}')
        update_user(message.peer_id, server.name, server.flag, url, key[0], key[1], user.refs, user.ref_balance, user.referal, user.balance, user.is_admin, user.end_date)
        update_server(url, server.name, server.flag, server.slots-1)

        await message.answer('✅Вставьте отправленный ниже токен в приложение Outline, и подключайтесь к вашему клубу интернета!', keyboard=EMPTY_KEYBOARD)
        await message.answer(f'{key[1]}')

        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})
    else:
        keyboard = Keyboard()
        keyboard.add(Text('🚀Новый токен'))
        
        await message.answer('Не верный ввод! Перед тем как продолжить работу после смены страны нужно обновить токен.', keyboard=keyboard)


@my_club_labeler.private_message(text="📃Инструкция")
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
        
    await message.answer('📝Для начала, нужно скачать наше приложение, выберите вашу платформу:', keyboard=keyboard)