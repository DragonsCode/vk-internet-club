from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink, EMPTY_KEYBOARD

from config import api, state_dispenser, labeler, scheduler, ADMIN_CHAT
from database.database import insert_user, create_tables, update_user, get_user
from functions.check_sub import sub_end_schedule
from handlers import donut_labeler, my_club_labeler, tariffs_labeler, admin_labeler, instructions_labeler, ref_labeler

labeler.load(donut_labeler)
labeler.load(my_club_labeler)
labeler.load(tariffs_labeler)
labeler.load(admin_labeler)
labeler.load(instructions_labeler)
labeler.load(ref_labeler)

bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

scheduler.start()


@bot.on.message(text="/id")
async def get_id(message: Message):
    await message.answer(f'peer_id: {message.peer_id}')


@bot.on.private_message(text="Отзывы")
async def private_message_handler(message: Message):
    await message.answer("🔥Свой собственный клуб интернета получили уже десятки пользователей, радуются и пишут отзывы\n\n👀Несколько я прикрепил, а остальные - читайте тут:\nhttps://vk.com/topic-211717723_48984252")


@bot.on.private_message()
async def smth(message: Message):
    insert_user(message.peer_id)

    keyboard = Keyboard()
    keyboard.add(Text('🔮Мой клуб', {'cmd': 'club'}))
    keyboard.row()
    keyboard.add(Text("👨‍💼Партнерка"))
    keyboard.row()
    keyboard.add(OpenLink('https://vk.me/homa_nobi', '🆘Помощь'))

    ref = message.ref
    if ref and ref.isdigit():
        if int(ref) == message.peer_id:
            # if {ref} id is user_id (Cheating)
            await message.answer('🔺Главное меню. Для работы используйте кнопки ниже', keyboard=keyboard)
            return
        
        user = get_user(message.peer_id)
        if user.referal:
            # if user already has a referer
            await message.answer('🔺Главное меню. Для работы используйте кнопки ниже', keyboard=keyboard)
            return
        
        is_group = 1 #await bot.api.groups.is_member(188552039, int(ref))
        referal = get_user(int(ref))
        print(referal)
        if is_group and referal:
            # if success

            update_user(
                message.peer_id,
                user.server,
                user.flag,
                user.url,
                user.token,
                user.access,
                user.refs,
                user.ref_balance,
                int(ref),
                user.balance,
                user.is_admin,
                user.end_date
            )
            update_user(
                int(ref),
                referal.server,
                referal.flag,
                referal.url,
                referal.token,
                referal.access,
                referal.refs + 1,
                referal.ref_balance,
                referal.referal,
                referal.balance,
                referal.is_admin,
                referal.end_date
            )
            await api.messages.send(
                peer_id=ADMIN_CHAT,
                message=f'[id{ref}|Пользователь] пригласил [id{message.peer_id}|друга]',
                random_id=0
            )
        else:
            pass
            # if User with id {ref} does not exist in this bot

    await message.answer('🔺Главное меню. Для работы используйте кнопки ниже', keyboard=keyboard)


create_tables()
sub_end_schedule()
bot.run_forever()
