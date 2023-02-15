from django.contrib import admin

from reviews.models import Comment, Review, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'bio',
        'role',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'score',
        'text',
        'pub_date',
    )
    list_filter = ('title', 'pub_date',)
    search_fields = ('title', 'author', 'review', 'text')


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'review',
        'text',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = ('author', 'review', 'text')


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
