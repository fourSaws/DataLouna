from typing import BinaryIO, Union
from urllib.error import HTTPError
from urllib.request import urlopen

import requests
from dataTypes import *

apiUrl = "http://127.0.0.1:8000/api"

'''
________________________________________________________________
Article methods
'''


def getArticle(id: int) -> Union[Article, None]:
    resp = requests.get(apiUrl + "/getArticle", params={'id': id})
    if resp.status_code == 400:
        return None
    data = resp.json()
    article = Article(
        id=int(data['id']),
        title=str(data['title']),
        text=str(data['text']),
        photoPath=str(data['photo']),
    )
    return article


def getArticlesByKeyWord(keyWord: str) -> Union[list[Article], None]:
    resp = requests.get(apiUrl + "/getArticlesByKeyWords", params={'word': keyWord})
    if resp.status_code == 400:
        print(
            "================================================================================"
        )
        print("getArticlesByKeyWord | keyWord = " + keyWord + " | 400 error")
        print(
            "================================================================================"
        )
        return None
    data = resp.json()
    articles = []
    for i in data:
        articles.append(
            Article(
                id=int(i['id']),
                title=str(i['title']),
                text=str(i['text']),
                photoPath=str(i['photo']),
            )
        )
    return articles


def getArticlesByNode(nodeId: int) -> Union[list[Article], None]:
    resp = requests.get(apiUrl + "/getArticlesByNode", params={'node_id': nodeId})
    if resp.status_code == 400:
        return None
    data = resp.json()
    articles = []
    for i in data:
        articles.append(
            Article(
                id=int(i['id']),
                title=str(i['title']),
                text=str(i['text']),
                photoPath=str(i['photo']),
            )
        )
    return articles


'''
________________________________________________________________
Category methods
'''


def getChildren(parrentId: int = None) -> Union[list[CategoryNode], None]:
    if parrentId != None:
        resp = requests.get(apiUrl + "/getChildren", params={'parent_id': parrentId})
    else:
        resp = requests.get(apiUrl + "/getChildren")
    if resp.status_code == 400:
        return None
    data = resp.json()
    categories = []
    for i in data:
        categories.append(
            CategoryNode(
                id=int(i['id']),
                name=str(i['name']),
                parentId=i['parent'],
                final=bool(i['final']),
            )
        )
    return categories


def getNode(categoryId: int) -> Union[CategoryNode, None]:
    resp = requests.get(apiUrl + "/getNode", params={'id': categoryId})
    if resp.status_code == 400:
        return None
    data = resp.json()[0]
    category = CategoryNode(
        id=int(data['id']),
        name=str(data['name']),
        parentId=data['parent'],
        final=bool(data['final']),
    )
    return category


def getPhoto(url: str) -> Union[BinaryIO, None]:
    try:
        return urlopen('http://127.0.0.1:8000/media/' + url).read()
    except HTTPError:
        return None
