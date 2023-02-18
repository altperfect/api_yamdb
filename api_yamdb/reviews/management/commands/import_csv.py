import csv
from api_yamdb.settings import BASE_DIR
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
    GenreTitle: "genre_title.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv"
}
class Command(BaseCommand):
    help = "Импорт данных из файлов csv в базу данных"

    def handle(self, *args, **options):
        for base in CSV_DICT.items():
            with open(
                f"{BASE_DIR}/static/data/{base}"
            ) as csv_files:
                csv_reader = csv.DictReader(csv_files)
            csv_reader.save()
