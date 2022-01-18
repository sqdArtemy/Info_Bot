from telegram import Update, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .models import User, Language, Questionnaire, Link, Category


def get_id(update: Update):  # returns user`s id
    try:
        return update.effective_message.chat_id
    except:
        raise IndexError


def get_item(update: Update, option):  # returns needed user`s attribute from DB
    try:
        object = User.objects.filter(tg_id=get_id(update)).get()
        field_object = User._meta.get_field(str(option))
        return getattr(object, field_object.attname)
    except:
        raise ValueError


def get_phrase(update: Update, option):  # returns particular phrase on a selected language
    try:
        language = Language.objects.filter(id=get_item(update, 'language')).get()
        field_object = Language._meta.get_field(str(option))
        return getattr(language, field_object.attname)
    except:
        raise ValueError


def keyboard_maker(update, type):  # makes keyboard when number of  buttons is variable
    items = type.objects.all()
    keyboard = []
    back = get_phrase(update, 'back')
    for item in items:
        keyboard.append([KeyboardButton(item.name)])
    if type != Questionnaire:
        keyboard.append([KeyboardButton(text=back)])
    else:
        keyboard.append([KeyboardButton(text=back),  KeyboardButton(get_phrase(update, 'back_category'))])
    return keyboard


def inline_keyboard_maker(update: Update, type, items=None):  # creates inline keyboard with appropriate buttons
    BUTTONS = {}
    keyboard = []
    if type == 'language':
        objects = Language.objects.all()
        for object in objects:
            text = str(object.name)
            BUTTONS[text] = text
            keyboard.append([InlineKeyboardButton(BUTTONS[text], callback_data=object.id)])
    elif type == 'info':
        objects = Language.objects.all()
        text = (objects.filter(id=get_item(update, 'language')).get()).chat_menu
        categories = Category.objects.all()
        for category in categories:
            BUTTONS[category.id] = category.name
            url = Link.objects.filter(category=category.id).get()
            keyboard.append([InlineKeyboardButton(BUTTONS[category.id], callback_data='group_link', url=url.link)])
    elif type == 'poll':
        for item in items:
            BUTTONS[item.id] = item.text
            keyboard.append([InlineKeyboardButton(BUTTONS[item.id], callback_data=item.id)])
    return InlineKeyboardMarkup(keyboard)


def message_sender(update: Update, text, keyboard):
    update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True
        )
    )