from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# token = 'vk1.a.PdBxBthx3qG98nynYuoZb1fs0ns80iF_KAOfQDpAgIBQMD1zuC6iBheqpWH0YdoiwGkBeTzCoaiQS_xZmCcw5M_e7R7eiFdhquoceizjJdOYC7JzJaeZEn5Xn5ZgiRJnUht__phyFcRVViif9bDAbt9Q1YBKRZTi6CiWMPAg-EkY0FyD8qGV73ZRnvdkT3_N'
token = 'vk1.a.hUqTyzNvAohFJxnVN0TQrM8o_P4IkjDTwjY6LnGH2Ykny4BJkJooX2Q6SUSi4yfiERRq7bwzwvmMTLN4P1bkOUV0QCVHzpkUnDvrhlumdgi_0z9eQkRJ2SjwMtHUzkFhUHP3I6kEZ0jIC-RJMdiCU5hmyvLfoXw1r-f_4pnQ2rRKOD5DX3XuZxURKDNpbepNWubSgThAgBAMYtwgo0-NgQ'

api = API(token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

scheduler = AsyncIOScheduler()

ADMIN_CHAT = 2000000003
