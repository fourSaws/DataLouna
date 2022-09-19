
from telebot import *
from telebot.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from mytoken import token
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
    root = getChildren()[0]
    # ---------------------------------------------------------------
    if root is None:
        print("__ ", message.chat.id)
        bot.send_message(message.from_user.id, "Error!!!")
        return
    children = getChildren(root.id)
    # ---------------------------------------------------------------
    if children is None:
        print("__ ", message.chat.id)
        bot.send_message(message.from_user.id, "Error!!!")
        return
    for i in children:
        # ---------------------------------------------------------------
        if i is None:
            bot.send_message(message.from_user.id, "Error!!!")
            return
        markup.add(
            InlineKeyboardButton(text=i.name,
                                 callback_data="c\0" + str(int(i.final)) +  # type and final
                                               "\0" + str(i.id) +  # id
                                               "\0" + str(i.parentId)))  # parentId
    bot.send_message(message.from_user.id, root.name + "\n\nКатегории", reply_markup=markup)


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


@bot.callback_query_handler(func=lambda call: call.data.split('\0')[0] == 'c')
def categoryCallback(call: CallbackQuery):
    """

    :param call:
    :return:
    """
    markup = InlineKeyboardMarkup()
    cbdata = call.data
    cbdata = cbdata.split('\0')
    if int(cbdata[1]):
        articles = getArticlesByNode(int(cbdata[2]))
        # ---------------------------------------------------------------
        if articles is None:
            print("__ ", call.message.chat.id)
            bot.send_message(call.from_user.id, "Error!!!")
            return
        for article in articles:
            # ---------------------------------------------------------------
            if article is None:
                bot.send_message(call.from_user.id, "Error!!!")
                return
            markup.add(
                InlineKeyboardButton(text=article.title,
                                     callback_data="a\0" + str(article.id) +  # id
                                                   "\0" + cbdata[2]))  # parentId
        node = getNode(int(cbdata[2]))
        parentId = node.parentId
        messageText = node.name
        node = getNode(parentId)
        markup.add(
            InlineKeyboardButton(text="Назад",
                                 callback_data="c\0" + str(int(node.final)) +  # type and final
                                               "\0" + str(node.id) +  # id
                                               "\0" + str(node.parentId)))  # parentId
        while True:
            if parentId is None:
                break
            node = getNode(parentId)
            parentId = node.parentId
            messageText = f'{node.name} → {messageText}'
        messageText = messageText + "\n\nСтатьи:"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=messageText, reply_markup=markup)
    else:
        categories = getChildren(int(cbdata[2]))
        if categories is None:
            print("__ ", call.from_user.id)
            bot.send_message(call.from_user.id, "Error!!!")
            return
        for category in categories:
            # ---------------------------------------------------------------
            if category is None:
                bot.send_message(call.from_user.id, "Error!!!")
                return
            markup.add(
                InlineKeyboardButton(text=category.name,
                                     callback_data="c\0" + str(int(category.final)) +  # type and final
                                                   "\0" + str(category.id) +  # id
                                                   "\0" + str(category.parentId)))  # parentId
        node = getNode(int(cbdata[2]))
        parentId = node.parentId
        messageText = node.name
        if parentId != None:
            markup.add(
                InlineKeyboardButton(text="Назад",
                                     callback_data="c\0" + str(int(node.final)) +  # type and final
                                                   "\0" + str(node.id) +  # id
                                                   "\0" + str(node.parentId)))  # parentId
        while True:
            if parentId is None:
                break
            node = getNode(parentId)
            parentId = node.parentId
            messageText = f'{node.name} → {messageText}'

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=messageText + "\n\nКатегории:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split('\0')[0] == 'a')
def articleCallback(call: CallbackQuery):
    markup = InlineKeyboardMarkup()
    cbdata = call.data
    cbdata = cbdata.split('\0')
    article = getArticle(int(cbdata[1]))
    # ---------------------------------------------------------------
    if article is None:
        print("__ ", call.message.chat.id)
        bot.send_message(call.from_user.id, "Error!!!")
        return
    bot.delete_message(call.message.chat.id, call.message.id)
    node = getNode(int(cbdata[2]))
    # ---------------------------------------------------------------
    if node is None:
        print("__ ", call.message.chat.id)
        bot.send_message(call.from_user.id, "Error!!!")
        return
    markup.add(InlineKeyboardButton(text="Назад",
                                     callback_data="c\0" + str(int(node.final)) +  # type and final
                                                   "\0" + str(node.id) +  # id
                                                   "\0" + str(node.parentId)))  # parentId))
    messageText = f'*{article.title}*\n\n{article.text}'
    img = getPhoto(article.photoPath)
    if img:
        bot.send_photo(call.message.chat.id, img, caption=messageText, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id,  messageText, reply_markup=markup, parse_mode="Markdown")

'''
________________________________________________________________________________________________________________________
Keyboard buttons
________________________________________________________________________________________________________________________
'''

bot.infinity_polling()

