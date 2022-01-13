from django.contrib import admin
from bot.models import Category, Publication, Language, User, Question, KeyWord, Link, Questionnaire, Answer, QuestionPoll


class InlineKeyword(admin.StackedInline):
    model = KeyWord

class InlineAnswer(admin.StackedInline):
    model = Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_dispaly = ('name', 'gender',),


@admin.register(Publication)
class PublicationAdmmin(admin.ModelAdmin):
    list_display = ('category', 'topic', 'language')
    inlines = [InlineKeyword]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'name', 'phone', 'language')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'time')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')


@admin.register(QuestionPoll)
class QuestionPollAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'text')
    inlines = [InlineAnswer]