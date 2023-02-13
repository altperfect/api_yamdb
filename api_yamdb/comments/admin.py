from django.contrib import admin

from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'review',
        'text',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = ('author', 'review', 'text')


admin.site.register(Comment, CommentAdmin)
