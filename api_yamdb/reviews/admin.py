from django.contrib import admin

from reviews.models import Review


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


admin.site.register(Review, ReviewAdmin)
