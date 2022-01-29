from telegram import *
from telegram.ext import *
import telegram
from .models import Language, User, Question, Category, Publication, KeyWord, Link, Questionnaire, QuestionPoll, Answer
from django.dispatch import receiver
from django.db.models.signals import post_save
from .functions import get_id, get_item, keyboard_maker, get_phrase, inline_keyboard_maker, message_sender
from django.conf import settings
from core import local_settings

bot = Bot(token=settings.TOKEN)  # telegram bot
# conversation states
(LANGUAGE, NAME, PHONE, QUESTION, MENU, QUESTION_VERIFICATION, CATEGORY, KEY_WORDS, POLL_HANDLER, POLL, SUGGESTION,
 GENDER, AGE, MARRIAGE, HEIGHT, WEIGHT) = range(16)


def start(update: Update, context: CallbackContext, *args, **kwargs, ):  # greets users and asks to choose language
    try:
        chat_id = get_id(update)
        try:
            user, _ = User.objects.get_or_create(tg_id=chat_id)
        except FileNotFoundError:
            raise FileNotFoundError
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'greetings'), reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'language_selection'),
                         reply_markup=inline_keyboard_maker(update, 'language'))
        return LANGUAGE
    except TelegramError:
        raise TelegramError


def ask_name(update: Update, context: CallbackContext):  # receives name from user and ask phone
    try:
        chat_id = get_id(update)
        text = update.effective_message.text
        anonymous = get_phrase(update, 'anonymous')
        if not any(map(str.isdigit, text)) or text == anonymous:
            if text == anonymous:
                user = User.objects.filter(tg_id=chat_id).get()
                if not user.is_anonymous:
                    User.objects.filter(tg_id=chat_id).update(is_anonymous=True)
                    name = ('Anonymous user #%s' % (int(User.objects.filter(is_anonymous=True).count())))
                else:
                    name = user.name
            else:
                name = text
                User.objects.filter(tg_id=chat_id).update(is_anonymous=False)
            User.objects.filter(tg_id=chat_id).update(name=name)
            bot.send_message(  # sends message with inline keyboard asking for a phone number
                chat_id=chat_id,
                text=get_phrase(update, 'phone_ask'),
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text=get_phrase(update, 'send_contact'), request_contact=True),
                            KeyboardButton(text=get_phrase(update, 'skip'))
                        ]
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=True,
                )
            )
            return PHONE
        else:
            update.message.reply_text(text=get_phrase(update, 'numbers_name'))
    except TelegramError:
        raise TelegramError


def ask_phone(update: Update, context: CallbackContext):  # receives phone from user and goes to menu
    try:
        text = update.effective_message.text
        text = text.replace('+', '')
        codes = ('33', '55', '77', '88', '90', '91', '93', '94', '95', '97', '98', '99')
        if (any(map(str.isdecimal, text)) and len(text) == 12 and (text[3:5] in codes)) or text == get_phrase(update,
                                                                                                              'skip'):
            chat_id = get_id(update)
            User.objects.filter(tg_id=chat_id).update(phone=text)
            bot.send_message(chat_id=chat_id, text=get_phrase(update, 'successful_registration'))
            menu(update)
            return MENU
        else:
            update.message.reply_text(text=get_phrase(update, 'incorrect_phone'))
    except TelegramError:
        raise TelegramError


def menu(update: Update):  # displays main menu to the user
    try:
        text = get_phrase(update, 'menu')
        bot.send_message(chat_id=get_id(update), text=text, reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=get_phrase(update, 'category_menu')),
                    KeyboardButton(text=get_phrase(update, 'video'))
                ],
                [
                    KeyboardButton(text=get_phrase(update, 'question_menu')),
                    KeyboardButton(text=get_phrase(update, 'chat_menu')),
                    KeyboardButton(text=get_phrase(update, 'info_menu')),
                    KeyboardButton(text=get_phrase(update, 'suggestion'))
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
            )
        )
    except TelegramError:
        raise TelegramError


def question(update: Update, context: CallbackContext):  # proceeds user`s questions
    chat_id = get_id(update)
    text = update.message.text
    if text != get_phrase(update, 'back'):
        User.objects.filter(tg_id=chat_id).update(question=text)
        text = f"{get_phrase(update, 'check_question')} {text}"
        keyboard = [
            [KeyboardButton(get_phrase(update, 'yes_q')), KeyboardButton(get_phrase(update, 'no_q'))],
            [KeyboardButton(get_phrase(update, 'back'))],
        ]
        message_sender(update, text=text, keyboard=keyboard)
        return QUESTION_VERIFICATION
    else:
        menu(update)
        return MENU


# finds all posts which have same keywords with user`s keywords
def post_finder(update: Update, context: CallbackContext):
    text = update.message.text
    back = get_phrase(update, 'back')
    back_category = get_phrase(update, 'back_category')
    if text != back and text != back_category:
        posts = []
        back_button = [KeyboardButton(text=back)]
        user_keywords = text.split(' ')

        def no_posts():  # if there is no publication bot will send this message
            keyboard = [[KeyboardButton(text=get_phrase(update, 'question_menu'))], back_button]
            message_sender(update, text=get_phrase(update, 'no_posts'), keyboard=keyboard)
            return MENU

        try:
            publications = Publication.objects.filter(language=get_item(update, 'language'),
                                                      category=get_item(update, 'chosen_category'))
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
                        text = ''.join(
                            ['*', post.topic, '*', '\n\n', post.text, '\n', '*', get_phrase(update, 'reference_link'),
                             '*', ': ', post.link])
                        image = open(post.image.path, 'rb')
                        bot.send_photo(
                            chat_id=get_id(update),
                            photo=image.read(),
                            caption=text,
                            parse_mode=telegram.ParseMode.MARKDOWN
                        )
                    except TelegramError:
                        raise TelegramError
                posts = []
                return MENU
            else:
                no_posts()
        except FileNotFoundError:
            no_posts()
    elif text == back:
        menu(update)
        return MENU
    elif text == back_category:
        update.message.reply_text(text=get_phrase(update, 'categories'), reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard_maker(update, Category),
            resize_keyboard=True,
            )
        )
        return CATEGORY


# send questions of the questionnaire and then displaying results
def polls_selection(update: Update, context: CallbackContext):
    text = update.message.text
    back = get_phrase(update, 'back')  # phrase of "back" button
    if text != back:
        chat_id = get_id(update)
        poll_object = Questionnaire.objects.filter(name=text)
        poll = poll_object.get()

        # set counter values to default values
        User.objects.filter(tg_id=chat_id).update(poll=poll, score=0)
        User.objects.filter(tg_id=chat_id).update(number_answers=poll.question_amount)

        # creating text of the answer
        questions = QuestionPoll.objects.filter(questionnaire=poll)
        text = f" {get_phrase(update, 'poll_selected')}  {poll.name}"
        message_sender(update, text=text, keyboard=[[KeyboardButton(back)]])
        answers = Answer.objects.filter(question=questions[0])

        bot.send_message(chat_id=chat_id, text=questions[0].text,
                         reply_markup=inline_keyboard_maker(update, 'poll', answers))
        return POLL_HANDLER
    elif back:
        menu(update)
        return MENU


def contact_receiver(update: Update, context: CallbackContext):  # gets phone number from user`s contact
    chat_id = get_id(update)
    phone = update.effective_message.contact.phone_number
    User.objects.filter(tg_id=chat_id).update(phone=phone)
    bot.send_message(chat_id=chat_id, text=get_phrase(update, 'successful_registration'))
    menu(update)
    return MENU


# checks if question was answered and sends response
@receiver(post_save, sender=Question)
def question_observe(sender, instance: Question, **kwargs):
    try:
        question = instance
        user_language = (User.objects.filter(tg_id=question.user_id).get()).language
        language = Language.objects.filter(name=user_language).get()
        if question.status is False and question.answer:
            text = f"{language.answered_question}\n{language.question} {question.text}\n{language.answer} {question.answer}"
            bot.send_message(chat_id=question.user_id, text=text)
            Question.objects.filter(id=question.id).update(status=True)  # set status to "answered"
    except TelegramError:
        raise TelegramError


@receiver(post_save, sender=Publication)  # if there is new publication, bot sends it to the group
def publication_sender(sender, instance: Publication, **kwargs):
        text = f"*{instance.topic}*\n\n{instance.text}\n*{instance.language.reference_link}*: {instance.link}"
        channel = Link.objects.filter(name='Channel_id').get()
        image = open(instance.image.path, 'rb')
        bot.send_photo(chat_id=channel.link, photo=image.read(), caption=text, parse_mode=telegram.ParseMode.MARKDOWN)


