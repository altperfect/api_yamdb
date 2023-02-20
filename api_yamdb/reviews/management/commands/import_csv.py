from csv import DictReader

from django.core.management.base import BaseCommand

from reviews.models import(
    User,
    Category,
    Genre,
    GenreTitle,
    Title,
    Review,
    Comment
)

CSV_DICT = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    GenreTitle: 'genre_title.csv',
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv"
}

class Command(BaseCommand):
    """
    Импорт данных из csv файлов в базу данных.
    Переходит в директорию, где хранится файл и сохраняет его.
    """
    help = "Импорт данных из файлов csv в базу данных"

    def handle(self, *args, **options):
        for model, table in CSV_DICT.items():
            with open(
                f"./static/data/{table}",
                "r", encoding="utf-8"
            ) as csv_files:
                reader = DictReader(csv_files)
