from django.utils.translation import activate
from .models import Language, User, Question, Category, Link, Questionnaire, QuestionPoll, Answer, Suggestion
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, TelegramError
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, \
    CommandHandler
from .functions import get_phrase, get_id, get_item, message_sender, inline_keyboard_maker, keyboard_maker
from .bot import menu, start, ask_name, ask_phone, question, contact_receiver, polls_selection, post_finder, bot
from .bot import MARRIAGE, AGE, MENU, NAME, HEIGHT, WEIGHT, GENDER, QUESTION, SUGGESTION, POLL, KEY_WORDS, CATEGORY, \
    LANGUAGE, QUESTION_VERIFICATION, PHONE, POLL_HANDLER


def gender_n_marriage_handler(update: Update, context: CallbackContext):
    text = update.message.text
    user = User.objects.filter(tg_id=get_id(update))
    if text == get_phrase(update, 'male') or text == get_phrase(update, 'female'):
        user.update(gender=text)
        keyboard = [[KeyboardButton(get_phrase(update, 'yes')), KeyboardButton(get_phrase(update, 'no'))]]
        message_sender(update, text=get_phrase(update, 'marriage'), keyboard=keyboard)
        return MARRIAGE
    elif text == get_phrase(update, 'yes') or text == get_phrase(update, 'no'):
        user.update(mariage=text)
        update.message.reply_text(text=get_phrase(update, 'age'), reply_markup=ReplyKeyboardRemove())
        return AGE
    elif text == get_phrase(update, 'back'):
        menu(update)
        return MENU


def category_handler(update: Update, context: CallbackContext):  # checks if category was inputted
    try:
        text = update.message.text
        back = get_phrase(update, 'back')
        if text != back:
            categories = Category.objects.all()
            for category in categories:
                if text == category.name:
                    User.objects.filter(tg_id=get_id(update)).update(chosen_category=category)
                    text = f"{get_phrase(update, 'selected_category')} {category.name}"
                    keyboard = [
                        [KeyboardButton(get_phrase(update, 'poll_button')), KeyboardButton(get_phrase(update, 'find'))],
                        [KeyboardButton(back), KeyboardButton(get_phrase(update, 'back_category'))],
                    ]
                    message_sender(update, text=text, keyboard=keyboard)
                    return MENU
        else:
            menu(update)
            return MENU
    except TelegramError:
        raise TelegramError


def poll_handler(update: Update, context: CallbackContext):  # handle answers fo the questions of the poll
    query = update.callback_query
    data = query.data
    chat_id = get_id(update)
    answer = Answer.objects.filter(id=data).get()
    user = User.objects.filter(tg_id=chat_id)
    user.update(number_answers=user.get().number_answers-1)
    user.update(score=user.get().score + answer.points)
    poll = Questionnaire.objects.filter(id=get_item(update, 'poll'))
    questions = QuestionPoll.objects.filter(questionnaire=poll.get())
    if not user.get().number_answers <= 0:
        question = questions[poll.get().questions_number - user.get().number_answers]
        answers = Answer.objects.filter(question=question)
        query.edit_message_text(
            text=f'{question.text}',
            reply_markup=inline_keyboard_maker(update, 'poll', answers)
        )
    else:
        query.edit_message_text(text=(''.join([get_phrase(update, 'final_score'), str(user.get().score)])))
        bot.send_message(chat_id=chat_id, text=(''.join([get_phrase(update, 'results'), '\n', poll.get().answers])))


def inline_callback_handler(update: Update, context: CallbackContext):  # handles callbacks from inline keyboard query
    query = update.callback_query
    data = query.data
    chat_id = get_id(update)
    language = Language.objects.filter(id=data).get()
    User.objects.filter(tg_id=chat_id).update(language=data)
    activate(language.code)
    bot.send_message(chat_id=get_id(update), text=get_phrase(update, 'name_ask'), reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_phrase(update, 'anonymous'))]],
        resize_keyboard=True,
    )
                     )
    query.edit_message_text(text=get_phrase(update, 'language_set'))
    return NAME


def suggestion_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text != get_phrase(update, 'back'):
        suggestion = Suggestion.objects.create(
            text=text,
            user_id=get_id(update),
        )
        update.message.reply_text(text=get_phrase(update, 'thanks_suggestion'))
    else:
        menu(update)
    return MENU


def message_handler(update: Update, context: CallbackContext):  # handles all messages from user
    chat_id = get_id(update)
    text = update.message.text
    back_button = KeyboardButton(text=get_phrase(update, 'back'))
    back_to_category = KeyboardButton(get_phrase(update, 'back_category'))

    """
    there are states, which check how to handle particular phrase and make response to them
    """

    if text == get_phrase(update, 'info_menu'):
        message_sender(update, text=get_phrase(update, 'info'), keyboard=[[back_button]])

    elif text == get_phrase(update, 'back'):
        menu(update)
        return MENU

    elif text == get_phrase(update, 'chat_menu'):
        update.message.reply_text(text=get_phrase(update, 'chat'), reply_markup=inline_keyboard_maker(update, 'info'))
        menu(update)

    elif text == get_phrase(update, 'question_menu'):
        keyboard = [
                       [KeyboardButton(get_phrase(update, 'male')), KeyboardButton(get_phrase(update, 'female'))],
                       [back_button]
                   ]
        message_sender(update, text=get_phrase(update, 'gender'), keyboard=keyboard)
        return GENDER

    elif text == get_phrase(update, 'no_q'):
        message_sender(update, text=get_phrase(update, 'ask_question'), keyboard=[[back_button]])
        return QUESTION

    elif text == get_phrase(update, 'suggestion'):
        message_sender(update, text=get_phrase(update, 'write_suggestion'), keyboard=[[back_button]])
        return SUGGESTION

    elif text == get_phrase(update, 'yes_q'):
        chat_id = get_id(update)
        user = User.objects.filter(tg_id=chat_id).get()
        question = Question.objects.create(
            user_id=chat_id,
            text=user.question,
            user_age=user.age,
            user_gender=user.gender,
            user_mariage=user.marriage,
            user_weight=user.weight,
            user_height=user.height,
        )
        bot.send_message(chat_id=chat_id, text=get_phrase(update, 'question_created'))
        menu(update)
        return MENU

    elif text == get_phrase(update, 'video'):
        url = Link.objects.filter(name='Video').get()
        text = f"{get_phrase(update, 'video_text')} {url.link}"
        message_sender(update, text=text, keyboard=[[back_button]])

    elif text == get_phrase(update, 'category_menu') or text == get_phrase(update, 'back_category'):
        message_sender(update, text=get_phrase(update, 'categories'), keyboard=keyboard_maker(update, Category))
        return CATEGORY

    elif text == get_phrase(update, 'find'):
        message_sender(update, text=get_phrase(update, 'key_words'), keyboard=[[back_button, back_to_category]])
        return KEY_WORDS

    elif text == get_phrase(update, 'poll_button'):
        try:
            polls = Questionnaire.objects.filter(category=get_item(update, 'chosen_category'))
        except:
            polls = 0
        if polls:
            message_sender(update, text=get_phrase(update, 'select_poll'),
                           keyboard=keyboard_maker(update, Questionnaire))
            return POLL
        else:
            message_sender(update, text=get_phrase(update, 'no_polls'), keyboard=[[back_button, back_to_category]])
            return MENU


class NumberHandler:  # this class constructs handlers for states, where inputs
    def __init__(self, phrase, field):
        self.phrase = phrase
        self.field = field

    def builder(self, update: Update, context: CallbackContext):
        text = update.message.text
        if any(map(str.isdecimal, text)):
            user = User.objects.filter(tg_id=get_id(update)).get()
            setattr(user, self.field, text)
            user.save()
            update.message.reply_text(text=get_phrase(update, self.phrase))
        else:
            update.message.reply_text(text=get_phrase(update, 'incorrect_data'))


# handlers, which should check number input
def age_handler(update: Update, context: CallbackContext):  # writes user`s age into DB if it is correct
    NumberHandler('weight', 'age').builder(update, context)
    return WEIGHT


def weight_handler(update: Update, context: CallbackContext):  # writes user`s weight into DB if it is correct
    NumberHandler('height', 'weight').builder(update, context)
    return HEIGHT


def height_handler(update: Update, context: CallbackContext):  # writes user`s age height DB if it is correct
    NumberHandler('ask_question', 'height').builder(update, context)
    return QUESTION


# conversation handler with states for dispatcher
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LANGUAGE: [CallbackQueryHandler(callback=inline_callback_handler)],
        NAME: [MessageHandler(Filters.text, ask_name)],
        PHONE: [MessageHandler(Filters.text, ask_phone), MessageHandler(Filters.contact, contact_receiver)],
        MENU: [MessageHandler(Filters.text, message_handler)],
        QUESTION: [MessageHandler(Filters.text, question)],
        QUESTION_VERIFICATION: [MessageHandler(Filters.text, message_handler)],
        CATEGORY: [MessageHandler(Filters.text, category_handler)],
        POLL: [MessageHandler(Filters.text, polls_selection)],
        KEY_WORDS: [MessageHandler(Filters.text, post_finder)],
        SUGGESTION: [MessageHandler(Filters.text, suggestion_handler)],
        POLL_HANDLER: [CallbackQueryHandler(callback=poll_handler), MessageHandler(Filters.text, message_handler)],
        GENDER: [MessageHandler(Filters.text, gender_n_marriage_handler)],
        MARRIAGE: [MessageHandler(Filters.text, gender_n_marriage_handler)],
        AGE: [MessageHandler(Filters.text, age_handler)],
        WEIGHT: [MessageHandler(Filters.text, weight_handler)],
        HEIGHT: [MessageHandler(Filters.text, height_handler)]
    },
    fallbacks=[MessageHandler(Filters.command, start)],
    allow_reentry=True,
)
