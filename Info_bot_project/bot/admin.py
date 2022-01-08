from django.contrib import admin
from django.db import models
from bot.models import Category, Publication, Language, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_dispaly = ('name', 'gender',)


@admin.register(Publication)
class PublicationAdmmin(admin.ModelAdmin):
    list_display = ('category', 'topic',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'name', 'phone', 'language')