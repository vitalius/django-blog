from blog.models import Post, Category, Comment
from django.contrib import admin
from django.forms import Textarea
from django.db import models

admin.site.register(Category)

def is_published(obj):
    return not obj.draft
is_published.short_description = 'Published'
is_published.boolean = True


def is_commentable(obj):
    return obj.comments_enable
is_commentable.short_description = 'Commentable'
is_commentable.boolean = True




def make_published(modeladmin, request, queryset):
    queryset.update(draft=False)
make_published.short_description = "Publish!!!"

def make_drafts(modeladmin, request, queryset):
    queryset.update(draft=True)
make_drafts.short_description = "Draft!!!"



def enable_comments(modeladmin, request, queryset):
    queryset.update(comments_enable=True)
enable_comments.short_description = "Enable comments"

def disable_comments(modeladmin, request, queryset):
    queryset.update(comments_enable=False)
disable_comments.short_description = "Disable comments"



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', is_published, is_commentable)
    list_display_links = ('title','pub_date')

    list_filter = ['pub_date']

    search_fields = ['title']
    date_hierarchy = 'pub_date'

    fieldsets = (
        ('Post', {
                'fields':(('title', 'draft', 'comments_enable'), 'body', 'category'),
                }),
        ('Date', {
                'fields':('pub_date',),
            })
        )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':80})},
    }

    actions = [make_published, make_drafts, enable_comments, disable_comments]

admin.site.register(Post, PostAdmin)






def shown(obj):
    return not obj.hide
shown.short_description = 'Shown?'
shown.boolean = True


def hide_comments(modeladmin, request, queryset):
    queryset.update(hide=True)
hide_comments.short_description = "Hide"

def show_comments(modeladmin, request, queryset):
    queryset.update(hide=False)
show_comments.short_description = "Show"


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date', shown)
    list_filter = ['pub_date', 'name']
    search_fields = ['body']
    date_hierarchy = 'pub_date'

    actions = [hide_comments, show_comments]

admin.site.register(Comment, CommentAdmin)
