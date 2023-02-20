from csv import DictReader

from django.core.management.base import BaseCommand

from reviews.models import(
    User,
    Category,
    Genre,
    Title,
    Review,
    Comment
)

CSV_DICT = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
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
                f"./static/data/{table}"
            ) as csv_files:
                csv_reader = DictReader(csv_files)
                model.objects.bulk_create(
                    model(**data) for data in csv_reader
                )
        self.stdout.write(self.style.SUCCESS('Данные загружены!'))

        with open(f"./static/data/genre_title.csv") as csv_file:
            csv_genre_title = DictReader(csv_file)
            model.objects.bulk_create(
                model(**data) for data in csv_genre_title
            )
        self.stdout.write(self.style.SUCCESS('Данные загружены!'))
