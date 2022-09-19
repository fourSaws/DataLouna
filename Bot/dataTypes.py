# import typing
from dataclasses import dataclass


@dataclass
class Article:
    id: int
    title: str  # короткое описание
    text: str  # Текст статьи
    photoPath: str  # url to photo


@dataclass
class CategoryNode:
    id: int
    name: str
    parentId: int  # nullable
    final: bool
