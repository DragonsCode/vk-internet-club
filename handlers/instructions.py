from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, KeyboardButtonColor, GroupEventType, GroupTypes

from config import api, state_dispenser, ADMIN_CHAT
from states import ctx, InstructionsData
from functions.vpn import new_key, del_key
from database.database import get_user, update_user, get_server, get_server_by_country, update_server, update_user


instructions_labeler = BotLabeler()
instructions_labeler.vbml_ignore_case = True
instructions_labeler.auto_rules = [rules.PeerRule(from_chat=False)]

links = {'Android': 'google.com', 'IOS': 'apple.com', 'Windows': 'bing.com', 'Mac': 'yandex.com'}


@instructions_labeler.private_message(state=InstructionsData.SERVER)
async def instruction_server(message: Message):
    if message.text == 'Connect':
        await state_dispenser.set(message.peer_id, InstructionsData.CONNECT)

        keyboard = Keyboard(one_time=True)
        servers = get_server(is_open=True)
        if not servers:
            await message.answer('No servers available')
        
        countries = []
        count = 0
        user = get_user(message.peer_id)

        for n, i in enumerate(servers):
            if i.name not in countries and i.name != user.server:
                countries.append(i.name)

                txt = f'{i.flag} {i.name} - {i.slots} слотов'
                count += 1

                data = ctx.get(message.peer_id)
                data[f'server_{n}'] = i
                data[f'server_{n}_in'] = txt

                keyboard.add(Text(txt))
        
        data['server_count'] = count
        ctx.set(message.peer_id, data)
        
        await message.answer('Выберите сервер', keyboard=keyboard)
    
    else:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Connect'))
        await message.answer('You have to connect, before using our service', keyboard=keyboard)


@instructions_labeler.private_message(state=InstructionsData.CONNECT)
async def instruction_connect(message: Message):
    countries = {}

    data = ctx.get(message.peer_id)
    count = data['server_count']
    
    for i in range(count):
        countries[data[f'server_{i}_in']] = data[f'server_{i}']

    if message.text in list(countries.keys()):
        flag = message.text.split(' - ')[0]
        country = flag.split(' ')
        country = country[1]
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

        data['token'] = key[1]
        ctx.set(message.peer_id, data)

        await state_dispenser.set(message.peer_id, InstructionsData.PLATFORM)

        platforms = ['Android', 'IOS', 'Windows', 'Mac']

        keyboard = Keyboard(inline=True)
        for i in platforms:
            keyboard.add(Text(i))
            if i == 'IOS':
                keyboard.row()
        
        await message.answer('Now you have to choose your platform', keyboard=keyboard)
    
    else:
        keyboard = Keyboard(one_time=True)
        servers = get_server(is_open=True)
        if not servers:
            await message.answer('No servers available')
        
        countries = []
        count = 0

        for n, i in enumerate(servers):
            if i.name not in countries:
                countries.append(i.name)

                txt = f'{i.flag} {i.name} - {i.slots} слотов'
                count += 1

                data = ctx.get(message.peer_id)
                data[f'server_{n}'] = i
                data[f'server_{n}_in'] = txt

                keyboard.add(Text(txt))
        
        data['server_count'] = count
        ctx.set(message.peer_id, data)
        
        await message.answer('You have to choose correct server!', keyboard=keyboard)


@instructions_labeler.private_message(state=InstructionsData.PLATFORM)
async def instruction_platform(message: Message):
    if message.text in ['Android', 'IOS', 'Windows', 'Mac']:
        await state_dispenser.set(message.peer_id, InstructionsData.DOWNLOAD)

        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Downloaded'))

        await message.answer(f'Download for {message.text}: {links.get(message.text, 0)}', keyboard=keyboard)
    
    else:
        platforms = ['Android', 'IOS', 'Windows', 'Mac']

        keyboard = Keyboard(inline=True)
        for i in platforms:
            keyboard.add(Text(i))
            if i == 'IOS':
                keyboard.row()
        
        await message.answer('You have to choose platform!', keyboard=keyboard)


@instructions_labeler.private_message(state=InstructionsData.DOWNLOAD)
async def instructions_token(message: Message):
    data = ctx.get(message.peer_id)

    if message.text == 'Downloaded':
        token = data['token']


        await state_dispenser.set(message.peer_id, InstructionsData.READY)

        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Ready'))

        await message.answer('Вставьте отправленный ниже токен', keyboard=keyboard)
        await message.answer(f'{token}')
    else:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Downloaded'))
        
        await message.answer('You have to download and press the button to continue!', keyboard=keyboard)


@instructions_labeler.private_message(state=InstructionsData.READY)
async def instruction_ready(message: Message):
    if message.text == 'Ready':
        await message.answer('Awesome! Enjoy with your club')

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

            await state_dispenser.delete(message.peer_id)
            ctx.set(message.peer_id, {})

        else:
            keyboard = Keyboard(inline=True)
            keyboard.add(Text('Годовая подписка'), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
            keyboard.add(Text('Месячная подписка'), color=KeyboardButtonColor.PRIMARY)

            await message.answer('😔Пока у вас нет собственного клуба интернета\n\n👀Только посмотрите, что вы получите:\n\n👉🏻Доступ к запрещенным сайтам (Canva, Instagram)\n👉🏻Высокую скорость работы\n👉🏻Скрытие вашего местоположения\n👉🏻100% защиту ваших данных\n\n💡Выберите срок оформления:', keyboard=keyboard)
    
    else:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Ready'))

        await message.answer('If you are done, press the button to continue', keyboard=keyboard)