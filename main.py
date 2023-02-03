from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink, EMPTY_KEYBOARD

from config import api, state_dispenser, labeler, scheduler
from database.database import insert_user, create_tables
from functions.check_sub import sub_end_schedule
from handlers import donut_labeler, my_club_labeler, tariffs_labeler, admin_labeler, instructions_labeler

labeler.load(donut_labeler)
labeler.load(my_club_labeler)
labeler.load(tariffs_labeler)
labeler.load(admin_labeler)
labeler.load(instructions_labeler)

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


# @bot.on.private_message(text='/nax')
# async def no_board(message: Message):
#     await message.answer('Netu nax', keyboard=EMPTY_KEYBOARD)

@bot.on.private_message(text="Реферальная система")
async def ref(message: Message):
    user_id = message.peer_id
    await message.answer(f"Приглашайте людей по вашей ссылке и получайте скидки!\nВаша ссылка: vk.me/intervpn?ref={user_id}")


@bot.on.private_message()
async def smth(message: Message):
    ref = message.ref
    if ref and ref.isdigit():
        if int(ref) == message.peer_id:
            await message.answer('Cheater!')
            return
        is_group = await bot.api.groups.is_member(188552039, int(ref))
        if is_group:
            await message.answer(f"Вы пришли по ссылке человека: {ref}")
        else:
            await message.answer(f'User with id {ref} does not exist in this bot')
    else:
        await message.answer("Привет")

@bot.on.private_message()
async def check_db(message: Message):
    insert_user(message.peer_id)
    await message.answer('Напишите команду "Мой клуб"')


create_tables()
sub_end_schedule()
bot.run_forever()
