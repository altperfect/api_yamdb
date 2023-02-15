from django.contrib import admin

from .models import Title, Category, Genre

class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'genre',
        'category'
    )
    list_filter = ('pub_date',)
    search_fields = ('name', 'description', 'genre', 'category')

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
