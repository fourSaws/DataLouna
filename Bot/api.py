from types import SimpleNamespace
from typing import BinaryIO, Union
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import quote

import variables
import requests
import telebot.types

from dataTypes import *
from variables import *
from datetime import datetime

from telebot.types import InputTextMessageContent, InputMediaPhoto

apiUrl = localServerPath + "/api"
# localServerPath = serverPath
# apiUrl = serverPath + "/api"
authToken = "Token " + authorization

def strIsNoneToInt(val: str):
    if val is None:
        return None
    else:
        return int(val)

# def strIsNoneToDate(val: str):


'''
________________________________________________________________
Article methods
'''


def getArticle(id: int = -1) -> Union[Article, None]:
    if id < 0:
        resp = requests.get(apiUrl + "/topArticles",
                            headers={'Authorization': authToken})
    else:
        resp = requests.get(apiUrl + "/getArticle", params={'id': id},
                            headers={'Authorization': authToken})
    if resp.status_code != 200:
        if resp.status_code == 400:
            print("================================================================================")
            print("getArticles | article = " + str(id) + " | No such article | 400 error")
            print("================================================================================")
        elif resp.status_code == 401:
            print("================================================================================")
            print("getArticles | article = " + str(id) + " | Not Authorised | 401 error")
            print("================================================================================")
        else:
            print("================================================================================")
            print("getArticles | article = " + str(id) + " | unknown " + str(resp.status_code) + " error")
            print("================================================================================")
        return None
    data = resp.json()[0]
    if data['photo'] == None:
        data['photo'] = ""
    article = Article(
        id=int(data['id']),
        title=str(data['title']),
        text=str(data['text']),
        photoPath=str(data['photo']),
        childList=[PreArticle(preArticle["id"], preArticle["title"]) for preArticle in data['links']]
    )
    return article


def getArticlesByKeyWord(keyWord: str) -> Union[list[Article], None]:
    resp = requests.get(apiUrl + "/getArticlesByKeyWords", params={'word': keyWord},
                        headers={'Authorization': authToken})
    if resp.status_code == 400:
        print("================================================================================")
        print("getArticlesByKeyWord | keyWord = " + keyWord + " | 400 error")
        print("================================================================================")
        return None
    if resp.status_code == 404:
        return None
    data = resp.json()
    articles = []
    print(data)
    for i in data:
        print(i['photo'])
        if i['photo'] == None:
            i['photo'] = ""
        articles.append(
            Article(
                id=int(i['id']),
                title=str(i['title']),
                text=str(i['text']),
                photoPath=str(i['photo']),
                childList=[]
            )
        )
    return articles

'''
________________________________________________________________
User methods
'''

# def userSubStatus(subStatus: int):


def createUser(chatId: int, subStatus: str = "ZERO" ) -> Union[int]:
    resp = requests.get(apiUrl + "/createUser", params={'chat_id': chatId, 'subscription_status': subStatus},
                        headers={'Authorization': authToken})
    if resp.status_code != 200:
        if resp.status_code == 400:
            print("================================================================================")
            print("createUser | chatId = " + str(chatId) + " | No such article | 400 error")
            print("================================================================================")
        elif resp.status_code == 401:
            print("================================================================================")
            print("createUser | chatId = " + str(chatId) + " | Not Authorised | 401 error")
            print("================================================================================")
        else:
            print("================================================================================")
            print("createUser | chatId = " + str(chatId) + " | unknown " + str(resp.status_code) + " error")
            print("================================================================================")
        return False
    return True

def getUser(chatId: int) -> Union[User, None]:
    resp = requests.get(apiUrl + "/getUser", params={'chat_id': chatId},
                        headers={'Authorization': authToken})
    if resp.status_code != 200:
        if resp.status_code == 404:
            print("================================================================================")
            print("getUser | chatId = " + str(chatId) + " | No such User | 404 error | server answer = " + str(resp.json()))
            print("================================================================================")
        elif resp.status_code == 401:
            print("================================================================================")
            print("getUser | chatId = " + str(chatId) + " | Not Authorised | 401 error")
            print("================================================================================")
        else:
            print("================================================================================")
            print("getUser | chatId = " + str(chatId) + " | unknown " + str(resp.status_code) + " error")
            print("================================================================================")
        return None
    data = resp.json()[0]
    # user = User(
    #     chatId=int(data['chat_id']),
    #     siteId=int(data['site_id']),
    #     subscriptionStatus=str(data['subscription_status']),
    #     subscriptionEndDate=str(data['subscription_end_date']),
    # )
    print(data)
    user = User(
        chatId=strIsNoneToInt(data['chat_id']),
        siteId=strIsNoneToInt(data['site_id']),
        subscriptionStatus=str(data['subscription_status']),
        subscriptionEndDate=(datetime.strptime(str(data['subscription_end_date']), '%Y-%m-%dT%H:%M:%S') if data.get('subscription_end_date') else None),
    )
    return user

'''
________________________________________________________________
Global methods
'''

def sendQuizAnswer(codedAnswere: str):
    resp = requests.get(apiUrl + "/sendQuizAnswer", params={'codeString': codedAnswere},
                        headers={'Authorization': authToken})


def getPhoto(url: str) -> Union[BinaryIO, None]:
    if url == '' or url is None:
        return None
    try:
        # print(localServerPath + quote(url))
        photo = urlopen(localServerPath + quote(url)).read()
        return photo
    except HTTPError:
        return None


def articleToMessage(article: Article) -> [InputTextMessageContent]:
    messageText = f'[📚]({serverPath + "/media/" + article.photoPath})*{article.title}*\n\n{article.text}'

    message = InputTextMessageContent(
        messageText,
        parse_mode="Markdown",
    )
    return message
