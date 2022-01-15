from pyexpat import model
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET, SET_NULL


class Category(models.Model):
    name = models.CharField('Category_name', max_length=50, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Language(models.Model):
    name = models.CharField('Language name', max_length=100, unique=True)
    code = models.CharField('Language code', max_length=10, blank=True)
    greetings = models.TextField('Greeting message', blank=True)
    name_ask = models.TextField('Asking for a name', blank=True)
    phone_ask = models.TextField('Asking for a phone', blank=True)
    menu = models.TextField('Menu message', blank=True)
    category_menu = models.TextField('Category button in the menu', blank=True)
    question_menu = models.TextField('"Ask a question" button ', blank=True)
    chat_menu = models.TextField('"Group-chat menu" button ', blank=True)
    info_menu =  models.TextField('"Information about us" button', blank=True)
    info = models.TextField('Information', blank=True)
    send_contact = models.TextField('"Send contact" button', blank=True)
    language_set = models.TextField('Particular language has been chosen', blank=True)
    successful_registration = models.TextField('Successful registatration', blank=True)
    back = models.TextField('Back button', blank=True)
    chat = models.TextField('Link to chat', blank=True)
    language_selection = models.TextField('Select a language', blank=True)
    ask_question = models.TextField('Ask a anonimus question', blank=True)
    check_question = models.TextField('Chek if question is correct', blank=True)
    yes = models.TextField('Yes',blank=True)
    no = models.TextField('No', blank=True)
    answered_question = models.TextField('Your question have been answered', blank=True)
    question = models.TextField('User`s question', blank=True)
    answer = models.TextField('Answer to the question', blank=True)
    question_created = models.TextField('Question was succesfully created', blank=True)
    categories = models.TextField('Choose category', blank=True)
    key_words = models.TextField('Write keyword in order to find publication', blank=True)
    reference_link = models.TextField('Link to the resource', blank=True)
    posts_found = models.TextField('There are posts on your request', blank=True)
    no_posts = models.TextField('There are no posts', blank=True)
    numbers_name = models.TextField('There are numbers in name', blank=True)
    incorrect_phone = models.TextField('Phone was inputed inproperly!', blank=True)
    video = models.TextField('Video-instruction', blank=True)
    video_text = models.TextField('Here is the link to the video', blank=True)
    select_poll = models.TextField('Select poll', blank=True)
    no_polls = models.TextField('There are no polls', blank=True)
    poll_button = models.TextField('"Select poll" buton', blank=True)
    selected_category = models.TextField('Menu for category', blank=True)
    find = models.TextField('Find posts', blank=True)
    points = models.TextField('Points for answer', blank=True)
    results = models.TextField('Results of poll', blank=True)
    poll_selected = models.TextField('Questionnaire have been selected', blank=True)
    back_category = models.TextField('Back to categories', blank=True)
    anonymous = models.TextField('"Stay Anonymous" button', blank=True)
    skip = models.TextField('"Skip" button', blank=True)
    suggestion = models.TextField('"Add suggestion" button', blank=True)
    thanks_suggestion = models.TextField('Thanks for suggestion!', blank=True)
    write_suggestion = models.TextField('Write your suggestion', blank=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Publication(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    topic = models.CharField('Publication`s topic', max_length=256)
    text = models.TextField('Pulication`s text', blank=True)
    link = models.CharField('Reference link', max_length=100)
    language = models.ForeignKey(Language, on_delete=PROTECT)

    def __str__(self) -> str:
        return f'{self.topic}'


class Questionnaire(models.Model):
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)
    name = models.CharField('Name of the questionnaire',max_length=256, unique=True)
    answers = models.TextField('Table with answer-points')

    def __str__(self) -> str:
        return f'{self.name}'


class User(models.Model):
    tg_id = models.CharField('User`s TG id', max_length=100, unique=True)
    name = models.CharField('User`s name', max_length=100, blank=True, null=True)
    phone = models.CharField('User`s phone', max_length=100, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=PROTECT, default=1)
    chosen_category = models.ForeignKey(Category, on_delete=SET_NULL, blank=True, null=True)
    question = models.TextField('User`s question', blank=True, null=True)
    poll = models.ForeignKey(Questionnaire, on_delete=SET_NULL, blank=True, null=True)
    is_anonymous = models.BooleanField('Is user anonymous?', default=False)

    def __str__(self) -> str:
        return f'{self.name}'


class Question(models.Model):
    user_id = models.CharField('User telegram ID', max_length=100)
    text = models.TextField('Text of the question')
    status = models.BooleanField('Is question answered ?', default=False)
    answer = models.TextField('Answer to the question', blank=True, null=True)
    time = models.DateTimeField('Asked at:', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id}'


class KeyWord(models.Model):
    publication = models.ForeignKey(Publication, on_delete=PROTECT)
    word = models.CharField('Keyword', max_length=256)

    def __str__(self) -> str:
        return f'{self.word}'

class Link(models.Model):
    name = models.CharField('Name of link', max_length=100)
    link = models.CharField('Link itself', max_length=100)
    category = models.ForeignKey(Category, on_delete=SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class QuestionPoll(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=CASCADE, null=True)
    text = models.TextField('Text of the question')


class Answer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=CASCADE, null=True)
    question = models.ForeignKey(QuestionPoll, on_delete=CASCADE, null=True)
    text = models.CharField('Text of the answer', max_length=256)
    points = models.IntegerField('Number of points for answer', null=True)


class Suggestion(models.Model):
    text = models.TextField('Text of suggestion')
    user_id = models.CharField('Telegram if of the user', max_length=100)