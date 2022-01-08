from django.db import models
from django.db.models.deletion import PROTECT


class Category(models.Model):
    name = models.CharField('Category_name', max_length=50, unique=True)
    gender = models.CharField('For Gender', max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'


class Publication(models.Model):
    category = models.ForeignKey(Category, on_delete=PROTECT)
    topic = models.TextField('Publication`s topic')
    text = models.TextField('Pulication`s text')
    link = models.CharField('Reference link', max_length=100, blank=True)

    def __str__(self) -> str:
        return f'{self.topic}'


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

    def __str__(self) -> str:
        return f'{self.name}'


class User(models.Model):
    tg_id = models.CharField('User`s TG id', max_length=100, unique=True)
    name = models.CharField('User`s name', max_length=100, blank=True, null=True)
    phone = models.CharField('User`s phone', max_length=100, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=PROTECT, default=1)
    chosen_category = models.ForeignKey(Category, on_delete=PROTECT, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'


