from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from django.db.models.expressions import F
from telegram import base


class Category(models.Model):
    name = models.CharField('Category_name', max_length=50, unique=True)
    gender = models.CharField('For Gender', max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'


class Language(models.Model):
    name = models.CharField('Language name', max_length=100, unique=True)
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
    key_words = models.TextField('Write keyword in order t find ublication', blank=True)
    reference_link = models.TextField('Link to the resource', blank=True)
    posts_found = models.TextField('There are posts on your request', blank=True)
    no_posts = models.TextField('There are no posts', blank=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Publication(models.Model):
    category = models.ForeignKey(Category, on_delete=PROTECT)
    topic = models.TextField('Publication`s topic')
    text = models.TextField('Pulication`s text')
    link = models.CharField('Reference link', max_length=100, blank=True)
    language = models.ForeignKey(Language, on_delete=PROTECT)

    def __str__(self) -> str:
        return f'{self.topic}'


class User(models.Model):
    tg_id = models.CharField('User`s TG id', max_length=100, unique=True)
    name = models.CharField('User`s name', max_length=100, blank=True, null=True)
    phone = models.CharField('User`s phone', max_length=100, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=PROTECT, default=1)
    chosen_category = models.ForeignKey(Category, on_delete=PROTECT, blank=True, null=True)
    question = models.TextField('User`s question', blank=True, null=True)

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
    word = models.TextField('Keyword')

    def __str__(self) -> str:
        return f'{self.word}'

class Link(models.Model):
    name = models.CharField('Name of link', max_length=100)
    link = models.CharField('Link itself', max_length=100)
    