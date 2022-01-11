from telegram import *
from telegram.ext import *
from Info_bot_project.settings import TOKEN
from bot.models import Language, User, Question, Category, Publication, KeyWord
from django.dispatch import receiver
from django.db.models.signals import post_save

bot = Bot(token=TOKEN)
#conversation states
NAME, PHONE, QUESTION, MENU, QUESTION_VERIFICATION, CATEGORY, KEY_WORDS = range(7)

def get_id(update: Update): # returns user`s id 
    try: return update.effective_message.chat_id
    except: raise IndexError

def get_item(update: Update, option, type): # returns nedeed user`s attribute from DB
    try:
        object = type.objects.filter(tg_id=get_id(update)).get()
        field_object = type._meta.get_field(str(option))
        return getattr(object, field_object.attname)
    except:
        raise ValueError

def get_language(update: Update): # returns language selected by user
    return get_item(update, 'language', User)

def get_phrase(update: Update, option): # returns particular phrase on a selected language
    try:
        language = Language.objects.filter(id=get_language(update)).get()
        field_object = Language._meta.get_field(str(option))
        return getattr(language, field_object.attname)
    except:
        raise ValueError

def user_maker(chat_id):  # creates user`s account in the table if it does not exist
    try: user, _ = User.objects.get_or_create(tg_id=chat_id,)
    except: KeyError

def inline_keyboard(update: Update, type): # creates inline keyboard with appropriate buttons
    objects = Language.objects.all()
    BUTTONS = {}
    keyboard = []
    if type == 'language':
        for object in objects:
            text = str(object.name)
            BUTTONS[text] = text
            keyboard.append([InlineKeyboardButton(BUTTONS[text], callback_data=object.id)])
        return InlineKeyboardMarkup(keyboard)
    elif type == 'info':
        text = (objects.filter(id=get_language(update)).get()).chat_menu
        BUTTONS[type] = text
        keyboard = [[InlineKeyboardButton(BUTTONS[type], callback_data='group_link', url='https://t.me/uicparsebot')]]
        return InlineKeyboardMarkup(keyboard)

def ask_name(update: Update, context: CallbackContext): # recieves name from userand ask phone
    try: 
        chat_id=get_id(update)
        text = update.effective_message.text
        User.objects.filter(tg_id=chat_id).update(name=text)
        
        bot.send_message(chat_id=chat_id, # sends message with keyboard asking for a phone number 
            text=get_phrase(update, 'phone_ask'),
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=get_phrase(update,'send_contact'), request_contact=True)]],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
        )   
        return PHONE
    except: raise ValueError

def ask_phone(update: Update, context: CallbackContext): # recieves phone from user 
    try:
        text = update.effective_message.text
        chat_id = get_id(update)
        User.objects.filter(tg_id=chat_id).update(phone=text)
        bot.send_message(chat_id=chat_id, text = get_phrase(update, 'successful_registration'))
        menu(update)
        return MENU
    except:
        raise IndexError

def start(update: Update,context: CallbackContext, *args, **kwargs,): # greets users
    try:
        chat_id = get_id(update)
        user_maker(chat_id)
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'greetings'), reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'language_selection'), reply_markup=inline_keyboard(update, 'language'))
        return NAME
    except:
        raise IndexError

def menu(update: Update): # displays main menu to the user   
    text = get_phrase(update, 'menu')
    bot.send_message(chat_id=get_id(update), text=text, reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=get_phrase(update, 'category_menu')),],
                [KeyboardButton(text=get_phrase(update,'question_menu')),
                 KeyboardButton(text=get_phrase(update,'chat_menu')),
                 KeyboardButton(text=get_phrase(update,'info_menu')),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )

def question(update: Update,conext: CallbackContext): # proceeds user`s questions   
    chat_id = get_id(update)
    text = update.message.text
    if text != get_phrase(update, 'back'):
        User.objects.filter(tg_id=chat_id).update(question=text)
        update.message.reply_text(text=(get_phrase(update, 'check_question') + ' ' + text), reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(get_phrase(update, 'yes')), KeyboardButton(get_phrase(update, 'no'))],
                [KeyboardButton(get_phrase(update, 'back'))],
            ],
            resize_keyboard=True
            )
        )
        return QUESTION_VERIFICATION
    else:
        menu(update)
        return MENU

def message_handler(update: Update, context: CallbackContext): # handles all messages from uses
    chat_id = get_id(update)
    text = update.message.text
    back_button = [KeyboardButton(text=get_phrase(update, 'back'))]
    if text == get_phrase(update, 'info_menu'):
        update.message.reply_text(text=get_phrase(update, 'info'), 
        reply_markup=ReplyKeyboardMarkup(keyboard=[back_button],resize_keyboard=True)
        )
    elif text == get_phrase(update, 'back'):
        menu(update)
    elif text == get_phrase(update, 'chat_menu'):
        update.message.reply_text(text=get_phrase(update, 'chat'),reply_markup=inline_keyboard(update, 'info'))
        menu(update)
    elif text == get_phrase(update, 'question_menu') or text == get_phrase(update, 'no'):
        update.message.reply_text(text=get_phrase(update, 'ask_question'), reply_markup=ReplyKeyboardMarkup(
            keyboard=[back_button],
            resize_keyboard=True
            )
        )
        return QUESTION
    elif text == get_phrase(update, 'yes'):
        chat_id = get_id(update)
        question = Question.objects.create(
            user_id = chat_id,
            text = (User.objects.filter(tg_id=chat_id).get()).question
        )
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'question_created'))
        menu(update)
        return MENU
    elif text == get_phrase(update, 'category_menu'):
        categories = Category.objects.all()
        category_buttons = []
        for category in categories:
            category_buttons.append(KeyboardButton(category.name))
        update.message.reply_text(text=get_phrase(update, 'categories'), reply_markup=ReplyKeyboardMarkup(
            keyboard=[category_buttons, back_button],
            resize_keyboard=True,
            )
        )
        return CATEGORY
    else:
        categories = Category.objects.all()
        for category in categories:
            if text == category.name:
                User.objects.filter(tg_id=get_id(update)).update(chosen_category=category.id)
                update.message.reply_text(text=(get_phrase(update,'key_words') + ' ' + category.name + ':'), 
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[back_button],
                        resize_keyboard=True,
                    )
                )
        return KEY_WORDS

def inline_callback_handler(update:Update, context: CallbackContext): # handles callbacks from inliane keyboard query   
    query = update.callback_query
    data = query.data
    chat_id = get_id(update)
    if len(data) == 1:
        bot.send_message(chat_id=get_id(update), text=get_phrase(update, 'name_ask'))
        User.objects.filter(tg_id=chat_id).update(language=data)
        query.edit_message_text(text=get_phrase(update, 'language_set'))

def contact_reciever(update: Update, context: CallbackContext): #gets phone number from user`s contact
    chat_id = get_id(update)
    phone = (update.effective_message.contact).phone_number
    User.objects.filter(tg_id=chat_id).update(phone=phone)
    bot.send_message(chat_id=chat_id, text = get_phrase(update, 'successful_registration'))
    menu(update)
    return MENU

def post_finder(update: Update, context: CallbackContext): # finds all posts wich have same keywords with user`s keywords
    text = update.message.text
    user_keywords = text.split(' ')
    publications = Publication.objects.filter(language=get_item(update,'language', User), category=get_item(update, 'chosen_category', User))
    if publications:
        update.message.reply_text(text=get_phrase(update, 'posts_found'))
        for publication in publications:
            keywords = KeyWord.objects.filter(publication=publication.id)
            for keyword in keywords:
                if keyword.word in user_keywords:
                    text = publication.topic + '\n\n' + publication.text + '\n' + get_phrase(update, 'reference_link') + ' ' + publication.link
                    update.message.reply_text(text = text)
    else:
        pass


# conversation handler with states for dispatcher
conversation_handler = ConversationHandler( 
    entry_points=[CommandHandler('start', start)],  
    states={
        NAME: [MessageHandler(Filters.text, ask_name),],
        PHONE: [MessageHandler(Filters.text, ask_phone), MessageHandler(Filters.contact, contact_reciever)],
        MENU: [MessageHandler(Filters.text, message_handler)],
        QUESTION: [MessageHandler(Filters.text, question)],
        QUESTION_VERIFICATION: [MessageHandler(Filters.text, message_handler)],
        CATEGORY: [MessageHandler(Filters.text, message_handler)],
        KEY_WORDS: [MessageHandler(Filters.text, post_finder)],
        },
    fallbacks=[MessageHandler(Filters.command, start)],
    allow_reentry=True
)

@receiver(post_save, sender=Question) # cheks if question was answered
def question_observe(sender, instance: Question, **kwargs):
    try:
        question = instance
        user_language = (User.objects.filter(tg_id=question.user_id).get()).language
        language = Language.objects.filter(name=user_language).get()
        if question.status == False and question.answer:
            text = (language.answered_question + '\n'+ language.question + ' ' + question.text + '\n' + language.answer + ' ' + question.answer)
            bot.send_message(chat_id=question.user_id, text=text)
            Question.objects.filter(id=question.id).update(status=True)
    except: 
        raise ValueError