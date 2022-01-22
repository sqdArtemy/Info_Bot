from .models import Category, QuestionPoll, Answer, Questionnaire
from modeltranslation.translator import TranslationOptions, register


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(QuestionPoll)
class QuestionPollTranslationOption(TranslationOptions):
    fields = ('text',)


@register(Answer)
class AnswerTranslationOption(TranslationOptions):
    fields = ('text',)


@register(Questionnaire)
class QuestionnaireTranslationOption(TranslationOptions):
    fields = ('name', 'answers')
