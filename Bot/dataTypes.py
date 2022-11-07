# import typing
from dataclasses import dataclass
from collections import namedtuple
import datetime
from types import SimpleNamespace

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
    chatId: int #id чата с пользователем в телеграме
    subscriptionStatus: str #статус подписки
    # При создании ZERO
    # при апдейте либо FIRST(Не оформил триал)
    # либо SECOND(Триал оформлен)
    # либо THIRD(Оформил (продлил?) подписку)
    # либо FOURTH(Карта удалена сразу)
    subscriptionEndDate: str #дата окончания даты подписки
    siteId: int #id ользователя на сайте
