from telegram import *
from telegram.ext import *
import telegram
from Info_bot_project.settings import TOKEN
from bot.models import Language, User, Question, Category, Publication, KeyWord, Link
from django.dispatch import receiver
from django.db.models.signals import post_save

bot = Bot(token=TOKEN) # telegram bot 
LANGUAGE, NAME, PHONE, QUESTION, MENU, QUESTION_VERIFICATION, CATEGORY, KEY_WORDS = range(8) #conversation states

def get_id(update: Update): # returns user`s id 
    try: return update.effective_message.chat_id
    except: raise IndexError

def get_item(update: Update, option): # returns nedeed user`s attribute from DB
    try:
        object = User.objects.filter(tg_id=get_id(update)).get()
        field_object = User._meta.get_field(str(option))
        return getattr(object, field_object.attname)
    except:
        raise ValueError

def get_language(update: Update): # returns language selected by user
    return get_item(update, 'language')

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
        url = Link.objects.filter(name='Group').get()
        BUTTONS[type] = text
        keyboard = [[InlineKeyboardButton(BUTTONS[type], callback_data='group_link', url=url.link)]]
        return InlineKeyboardMarkup(keyboard)

def ask_name(update: Update, context: CallbackContext): # recieves name from userand ask phone
    try: 
        chat_id=get_id(update)
        text = update.effective_message.text
        if not any(map(str.isdigit, text)):
            User.objects.filter(tg_id=chat_id).update(name=text)
            
            bot.send_message(chat_id=chat_id, # sends message with inline keyboard asking for a phone number 
                text=get_phrase(update, 'phone_ask'),
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text=get_phrase(update,'send_contact'), request_contact=True)]],
                    resize_keyboard=True,
                    one_time_keyboard=True,
                )
            )   
            return PHONE
        else:
            update.message.reply_text(text=get_phrase(update, 'numbers_name'))
    except: raise ValueError

def ask_phone(update: Update, context: CallbackContext): # recieves phone from user 
    try:
        text = update.effective_message.text
        text = text[text.find('+')+1:]
        codes = ['33','55','77','88','90','91','93','94','95','97','98','99']
        if(any(map(str.isdecimal, text)) and len(text)==12 and (text[3:5] in codes)):
            chat_id = get_id(update)
            User.objects.filter(tg_id=chat_id).update(phone=text)
            bot.send_message(chat_id=chat_id, text = get_phrase(update, 'successful_registration'))
            menu(update)
            return MENU
        else:
            update.message.reply_text(text=get_phrase(update, 'incorrect_phone'))
    except:
        raise IndexError

def start(update: Update,context: CallbackContext, *args, **kwargs,): # greets users
    try:
        chat_id = get_id(update)
        user_maker(chat_id)
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'greetings'), reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'language_selection'), reply_markup=inline_keyboard(update, 'language'))
        return LANGUAGE
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
        update.message.reply_text(text=(get_phrase(update, 'check_question')).join([' ', text]), reply_markup=ReplyKeyboardMarkup(
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
    try:
        text = update.message.text
    except:
        raise ValueError
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

def category_handler(update: Update, context: CallbackContext):
    try:
        text = update.message.text
    except: raise ValueError
    try:
        categories = Category.objects.all()
        for category in categories:
            if text == category.name:
                User.objects.filter(tg_id=get_id(update)).update(chosen_category=category.id)
                update.message.reply_text(text=('').join([get_phrase(update,'key_words'), ' ', category.name, ':']),
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text=get_phrase(update, 'back'))]],
                        resize_keyboard=True,
                    )
                )
        return KEY_WORDS
    except:
        raise TypeError



def inline_callback_handler(update:Update, context: CallbackContext): # handles callbacks from inliane keyboard query   
    query = update.callback_query
    data = query.data
    chat_id = get_id(update)
    if len(data) == 1:
        bot.send_message(chat_id=get_id(update), text=get_phrase(update, 'name_ask'))
        User.objects.filter(tg_id=chat_id).update(language=data)
        query.edit_message_text(text=get_phrase(update, 'language_set'))
        return NAME

def contact_reciever(update: Update, context: CallbackContext): #gets phone number from user`s contact
    chat_id = get_id(update)
    phone = (update.effective_message.contact).phone_number
    User.objects.filter(tg_id=chat_id).update(phone=phone)
    bot.send_message(chat_id=chat_id, text = get_phrase(update, 'successful_registration'))
    menu(update)
    return MENU

def post_finder(update: Update, context: CallbackContext): # finds all posts wich have same keywords with user`s keywords
    text = update.message.text
    posts = []
    back_button = [KeyboardButton(text=get_phrase(update, 'back'))]
    user_keywords = text.split(' ')
    publications = Publication.objects.filter(language=get_item(update,'language'), category=get_item(update, 'chosen_category'))
    for publication in publications:
        keywords = KeyWord.objects.filter(publication=publication.id)
        for keyword in keywords:
            if keyword.word in user_keywords and publication not in posts:
                posts.append(publication)
    if posts:
        update.message.reply_text(text=get_phrase(update, 'posts_found'), reply_markup=ReplyKeyboardMarkup(
            keyboard=[back_button],
            resize_keyboard=True,
            )
        )
        for post in posts:
            try:
                text = ('').join(['*', post.topic, '*','\n\n', post.text, '\n', '*',get_phrase(update, 'reference_link'), '*',': ', post.link])
                update.message.reply_text(text=text, parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                raise ValueError
        posts = []
        return MENU
    else:
        try:
            update.message.reply_text(text=get_phrase(update, 'no_posts'),reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=get_phrase(update,'question_menu'))],back_button],
                resize_keyboard=True,
                )
            )
            return MENU
        except:
            raise ValueError
                

# conversation handler with states for dispatcher
conversation_handler = ConversationHandler( 
    entry_points=[CommandHandler('start', start)],  
    states={
        LANGUAGE:[CallbackQueryHandler(callback=inline_callback_handler)],
        NAME: [MessageHandler(Filters.text, ask_name),],
        PHONE: [MessageHandler(Filters.text, ask_phone), MessageHandler(Filters.contact, contact_reciever)],
        MENU: [MessageHandler(Filters.text, message_handler)],
        QUESTION: [MessageHandler(Filters.text, question)],
        QUESTION_VERIFICATION: [MessageHandler(Filters.text, message_handler)],
        CATEGORY: [MessageHandler(Filters.text, category_handler)],
        KEY_WORDS: [MessageHandler(Filters.text, post_finder)],
        },
    fallbacks=[MessageHandler(Filters.command, start)],
    allow_reentry=True,
)


@receiver(post_save, sender=Question) # cheks if question was answered
def question_observe(sender, instance: Question, **kwargs):
    try:
        question = instance
        user_language = (User.objects.filter(tg_id=question.user_id).get()).language
        language = Language.objects.filter(name=user_language).get()
        if question.status == False and question.answer:
            text = ('').join([language.answered_question, '\n', language.question ,' ', question.text,'\n', language.answer,' ', question.answer])
            bot.send_message(chat_id=question.user_id, text=text)
            Question.objects.filter(id=question.id).update(status=True)
    except: 
        raise ValueError


@receiver(post_save, sender=Publication) # if there is new publication, bot sends it to the group
def publication_sender(sender, instance: Publication, **kwargs):
    try:
        text = ('').join(['*', instance.topic, '*', '\n\n', instance.text, '\n',  '*',(instance.language).reference_link, '*',': ', instance.link])
        channel = Link.objects.filter(name='Channel_id').get()
        bot.send_message(chat_id=channel.link, text=text, parse_mode=telegram.ParseMode.MARKDOWN)
    except: 
        raise ValueError