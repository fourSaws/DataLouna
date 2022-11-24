# import typing
from dataclasses import dataclass
from collections import namedtuple
from datetime import datetime
from types import SimpleNamespace
from typing import Union

@dataclass
class PreArticle:
    id: int
    title: str

@dataclass
class Article:
    id: int
    title: str  # короткое описание
    text: str  # Текст статьи
    photoPath: str  # url to photo
    childList: []


@dataclass
class User:
    chatId: Union[int, None] #id чата с пользователем в телеграме
    siteId: Union[int, None] #id ользователя на сайте
    subscriptionStatus: str #статус подписки
    # При создании ZERO
    # при апдейте либо FIRST(Не оформил триал)
    # либо SECOND(Триал оформлен)
    # либо THIRD(Оформил (продлил?) подписку)
    # либо FOURTH(Карта удалена сразу)
    # subscriptionEndDate: str #дата окончания даты подписки
    subscriptionEndDate: datetime #дата окончания даты подписки
