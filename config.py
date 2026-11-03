from runtime_config import required_env
from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

token = required_env('VK_BOT_TOKEN')

api = API(token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

scheduler = AsyncIOScheduler()

ADMIN_CHAT = 2000000003
