from vkbottle import CtxStorage, BaseStateGroup

ctx = CtxStorage()

class ChangedServerData(BaseStateGroup):

    SERVER = 0
    NEW_TOKEN = 1


class InstructionsData(BaseStateGroup):

    SERVER = 0
    CONNECT = 1
    PLATFORM = 2
    DOWNLOAD = 3
    READY = 4