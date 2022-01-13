from bot.models import Category, QuestionPoll, Answer
from modeltranslation.translator import TranslationOptions, register

@register(Category)
class CategotyTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(QuestionPoll)
class QuestionPollTranslationOption(TranslationOptions):
    fields = ('text', )


@register(Answer)
class AnswerTranslationOption(TranslationOptions):
    fields = ('text', )