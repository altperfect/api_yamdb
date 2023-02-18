from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User


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


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
    )
    list_filter = ('year',)
    search_fields = ('name', 'category', 'genre', 'description')


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
