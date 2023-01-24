from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink, EMPTY_KEYBOARD

from config import api, state_dispenser, labeler, ADMIN_CHAT

from handlers import donut_labeler, my_club_labeler, tariffs_labeler, admin_labeler

labeler.load(donut_labeler)
labeler.load(my_club_labeler)
labeler.load(tariffs_labeler)
labeler.load(admin_labeler)

bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)


@bot.on.message(text="/id")
async def get_id(message: Message):
    await message.answer(f'peer_id: {message.peer_id}')


@bot.on.private_message(text="/pf")
async def private_message_handler(message: Message):
    await message.answer("🔥Свой собственный клуб интернета получили уже десятки пользователей, радуются и пишут отзывы\n\n👀Несколько я прикрепил, а остальные - читайте тут:\nhttps://vk.com/topic-211717723_48984252")


@bot.on.private_message(text='/nax')
async def no_board(message: Message):
    await message.answer('Netu nax', keyboard=EMPTY_KEYBOARD)

bot.run_forever()
