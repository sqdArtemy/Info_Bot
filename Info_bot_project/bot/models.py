from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL


class Category(models.Model):
    name = models.CharField('Category_name', max_length=50, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Language(models.Model):
    name = models.CharField('Language name', max_length=256, unique=True)
    code = models.CharField('Language code', max_length=256, blank=True)
    greetings = models.CharField('Greeting message', max_length=256, blank=True)
    name_ask = models.CharField('Asking for a name', max_length=256, blank=True)
    phone_ask = models.CharField('Asking for a phone', max_length=256, blank=True)
    menu = models.CharField('Menu message', max_length=256, blank=True)
    category_menu = models.CharField('Category button in the menu', max_length=256, blank=True)
    question_menu = models.CharField('"Ask a question" button ', max_length=256, blank=True)
    chat_menu = models.CharField('"Group-chat menu" button ', max_length=256, blank=True)
    info_menu = models.CharField('"Information about us" button', max_length=256, blank=True)
    info = models.CharField('Information', max_length=256, blank=True)
    send_contact = models.CharField('"Send contact" button', max_length=256, blank=True)
    language_set = models.CharField('Particular language has been chosen', max_length=256, blank=True)
    successful_registration = models.CharField('Successful registatration', max_length=256, blank=True)
    back = models.CharField('Back button', max_length=256, blank=True)
    chat = models.CharField('Link to chat', max_length=256, blank=True)
    language_selection = models.CharField('Select a language', max_length=256, blank=True)
    ask_question = models.CharField('Ask a anonimus question', max_length=256, blank=True)
    check_question = models.CharField('Chek if question is correct', max_length=256, blank=True)
    yes_q = models.CharField('Yes in questions', max_length=256, blank=True)
    no_q = models.CharField('No, enter again', max_length=256, blank=True)
    answered_question = models.CharField('Your question have been answered', max_length=256, blank=True)
    question = models.CharField('User`s question', max_length=256, blank=True)
    answer = models.CharField('Answer to the question', max_length=256, blank=True)
    question_created = models.CharField('Question was succesfully created', max_length=256, blank=True)
    categories = models.CharField('Choose category', max_length=256, blank=True)
    key_words = models.CharField('Write keyword in order to find publication', max_length=256, blank=True)
    reference_link = models.CharField('Link to the resource', max_length=256, blank=True)
    posts_found = models.CharField('There are posts on your request', max_length=256, blank=True)
    no_posts = models.CharField('There are no posts', max_length=256, blank=True)
    numbers_name = models.CharField('There are numbers in name', max_length=256, blank=True)
    incorrect_phone = models.CharField('Phone was inputed inproperly!', max_length=256, blank=True)
    video = models.CharField('Video-instruction', max_length=256, blank=True)
    video_text = models.CharField('Here is the link to the video', max_length=256, blank=True)
    select_poll = models.CharField('Select poll', max_length=256, blank=True)
    no_polls = models.CharField('There are no polls', max_length=256, blank=True)
    poll_button = models.CharField('"Select poll" buton', max_length=256, blank=True)
    selected_category = models.CharField('Menu for category', max_length=256, blank=True)
    find = models.CharField('Find posts', max_length=256, blank=True)
    points = models.CharField('Points for answer', max_length=256, blank=True)
    results = models.CharField('Results of poll', max_length=256, blank=True)
    poll_selected = models.CharField('Questionnaire have been selected', max_length=256, blank=True)
    back_category = models.CharField('Back to categories', max_length=256, blank=True)
    anonymous = models.CharField('"Stay Anonymous" button', max_length=256, blank=True)
    skip = models.CharField('"Skip" button', max_length=256, blank=True)
    suggestion = models.CharField('"Add suggestion" button', max_length=256, blank=True)
    thanks_suggestion = models.CharField('Thanks for suggestion!', max_length=256, blank=True)
    write_suggestion = models.CharField('Write your suggestion', max_length=256, blank=True)
    age = models.CharField('Age of user', max_length=256, blank=True)
    gender = models.CharField('User`s gender', max_length=256, blank=True)
    mariage = models.CharField('Is user married?', max_length=256, blank=True)
    weight = models.CharField('User`s weight', max_length=256, blank=True)
    height = models.CharField('User`s height,', max_length=256, blank=True)
    male = models.CharField('Male', max_length=256, blank=True)
    female = models.CharField('Female', max_length=256, blank=True)
    incorrect_data = models.CharField('Input is incorrect', max_length=256, blank=True)
    yes = models.CharField('yes', max_length=256, blank=True)
    no = models.CharField('no', max_length=256, blank=True)
    final_score = models.CharField('User`s score for poll', max_length=256, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Publication(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    topic = models.CharField('Publication`s topic', max_length=256)
    text = models.TextField('Publication`s text', blank=True)
    link = models.CharField('Reference link', max_length=100)
    language = models.ForeignKey(Language, on_delete=PROTECT)

    def __str__(self) -> str:
        return f'{self.topic}'


class Questionnaire(models.Model):
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)
    name = models.CharField('Name of the questionnaire', max_length=256, unique=True)
    question_amount = models.IntegerField('Amount of questions', default=5)
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
    age = models.PositiveIntegerField('User`s age', blank=True, null=True)
    gender = models.CharField('User`s gender', max_length=256, blank=True, null=True)
    mariage = models.CharField('User`s marriage status', max_length=256, blank=True, null=True)
    weight = models.CharField('User`s weight', max_length=256, blank=True, null=True)
    height = models.CharField('User`s height', max_length=256, blank=True, null=True)
    score = models.PositiveIntegerField('Overall score for poll', blank=True, null=True)
    number_answers = models.PositiveIntegerField('Number of question', blank=True, default=0)

    def __str__(self) -> str:
        return f'{self.name}'


class Question(models.Model):
    user_id = models.CharField('User telegram ID', max_length=100)
    text = models.TextField('Text of the question')
    status = models.BooleanField('Is question answered ?', default=False)
    answer = models.TextField('Answer to the question', blank=True, null=True)
    time = models.DateTimeField('Asked at:', auto_now_add=True)
    user_age = models.PositiveIntegerField('User`s age')
    user_gender = models.CharField('User`s gender', max_length=256)
    user_mariage = models.CharField('User`s marriage status', max_length=256)
    user_weight = models.CharField('User`s weight', max_length=256)
    user_height = models.CharField('User`s height', max_length=256)

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
