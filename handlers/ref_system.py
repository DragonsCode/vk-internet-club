from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink

from config import api, ADMIN_CHAT
from database.database import get_user


ref_labeler = BotLabeler()
ref_labeler.vbml_ignore_case = True
ref_labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@ref_labeler.private_message(text="👨‍💼Партнерка")
@ref_labeler.private_message(payload={'ref': 'menu'})
async def ref_menu(message: Message):
    await message.answer('👁Совсем скоро появится партнерская программа!')