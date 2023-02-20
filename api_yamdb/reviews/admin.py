from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "review",
        "text",
        "pub_date",
    )
    list_filter = ("pub_date",)
    search_fields = ("author", "review", "text")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "score",
        "text",
        "pub_date",
    )
    list_filter = (
        "title",
        "pub_date",
    )
    search_fields = ("title", "author", "review", "text")


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
    )
    list_filter = ("year",)
    search_fields = ("name", "category", "genre", "description")


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "bio",
        "role",
    )
    search_fields = (
        "username",
        "role",
    )
    list_filter = ("username",)
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
