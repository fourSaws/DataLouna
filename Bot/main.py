from telebot import *
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InlineQuery,
)
from variables import *
from api import *

bot = TeleBot(token)
print("bot is running...")

'''
________________________________________________________________________________________________________________________
Commands
________________________________________________________________________________________________________________________
'''


@bot.message_handler(commands=['start'])
def send_hi(message: Message):
    print(message.chat.id, " - ", message.chat.first_name, " send /start")
    bot.send_message(message.chat.id, "Привет ✌️ ")


@bot.message_handler(commands=['faq'])
def send_category(message: types.Message):
    markup = InlineKeyboardMarkup()
    root = getArticle()
    # ---------------------------------------------------------------
    if root is None:
        print("__ ", message.chat.id)
        bot.send_message(message.from_user.id, "Error!!!")
        return
    # ---------------------------------------------------------------
    for i in root.childList:
        # ---------------------------------------------------------------
        if i is None:
            bot.send_message(message.from_user.id, "Error!!!")
            return
        markup.add(
            InlineKeyboardButton(
                text=i.title,
                callback_data="a" + chr(root.id) + chr(i.id),
            )
        )  # parentId
    bot.send_message(message.from_user.id, root.title + "\n\nКатегории", reply_markup=markup)


'''
________________________________________________________________________________________________________________________
Inline buttons
________________________________________________________________________________________________________________________
'''


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call: CallbackQuery):
#     markup = InlineKeyboardMarkup()
#     cbdata = call.data
#     if cbdata[0] == 'unseen':
#         bot.delete_message(call.message.chat.id, call.message.message_id)
# elif cbdata[0] == 'a':


@bot.callback_query_handler(func=lambda call: call.data[0] == 'a')
def articleCallback(call: CallbackQuery):
    markup = InlineKeyboardMarkup()
    cbdata = call.data[1:]
    article = getArticle(ord(cbdata[-1]))
    if len(cbdata) + 1 == 40:
        cbdata = cbdata[1:]
    # ---------------------------------------------------------------
    if article is None:
        print("__ ", call.message.chat.id)
        bot.send_message(call.from_user.id, "Error!!!")
        return
    bot.delete_message(call.message.chat.id, call.message.id)
    for i in article.childList:
        # ---------------------------------------------------------------
        if i is None:
            bot.send_message(call.message.chat.id, "Error!!!")
            return
        markup.add(
            InlineKeyboardButton(
                text=i.title,
                callback_data="a" + cbdata + chr(i.id),
            )
        )  # parentId
    if len(cbdata) == 2 and ord(cbdata[0]) != getArticle().id:
        markup.add(InlineKeyboardButton(text="На главную", callback_data="a" + chr(getArticle().id)))
    elif len(cbdata) >= 2:
        markup.add(InlineKeyboardButton(text="Назад", callback_data="a" + cbdata[:-1]))  # parentId))
    # print(article.photoPath)
    messageText = f'*{article.title}*\n\n{article.text}'
    img = getPhoto(article.photoPath)
    # print(img)
    if img:
        bot.send_photo(
            call.message.chat.id,
            img,
            caption=messageText,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            call.message.chat.id,
            messageText,
            reply_markup=markup,
            parse_mode="Markdown",
        )


'''
________________________________________________________________________________________________________________________
Keyboard buttons
________________________________________________________________________________________________________________________
'''

'''
________________________________________________________________________________________________________________________
Inline mode
________________________________________________________________________________________________________________________
'''


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inlineMode(data: InlineQuery):
    print(data)
    print(data.query)
    articles = getArticlesByKeyWord(data.query)
    print(articles)
    if articles == None:
        return
    inlineQuery = []
    cnt = 1
    for article in articles:
        inlineQuery.append(
            types.InlineQueryResultArticle(
                id=str(cnt),
                title=article.title,
                input_message_content=articleToMessage(article),
                description=article.text[:30] + "...",
            )
        )
        cnt += 1
    bot.answer_inline_query(data.id, inlineQuery)


bot.infinity_polling()

'''
________________________________________________________________________________________________________________________
Channel access
________________________________________________________________________________________________________________________
'''
