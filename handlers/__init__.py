from .donut_events import donut_labeler
from .my_club import my_club_labeler
from .tariffs import tariffs_labeler
from .admin import admin_labeler
# Если использовать глобальный лейблер, то все хендлеры будут зарегистрированы в том же порядке, в котором они были импортированы

__all__ = ("donut_labeler", "my_club_labeler", "tariffs_labeler", "admin_labeler")