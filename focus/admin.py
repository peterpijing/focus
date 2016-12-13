#coding=utf-8
from django.contrib import admin

# Register your models here.

from models import *

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id', 'pub_date', 'content', 'poll_num')

from django import forms
from django.db import models
# ‘formfield_overrides’ 可以更改字段默认的后台显示细节，这里我因为默认‘article’模块的‘content’字段尺寸太小，所以修改了一下尺寸。
class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(
                           attrs={'rows': 41,
                                  'cols': 100
                                  })},
    }
    list_display = ('title','pub_date', 'poll_num')


class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username','date_joined', 'profile')

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')



admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Author, AuthorAdmin)