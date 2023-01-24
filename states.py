from vkbottle import CtxStorage, BaseStateGroup

ctx = CtxStorage()

class ChangedServerData(BaseStateGroup):

    SERVER = 0
    NEW_TOKEN = 1
