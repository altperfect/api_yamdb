from csv import DictReader

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title, User

CSV_DICT = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv",
    "Genre_Title": "genre_title.csv",
}


def db_clear():
    """Очищает базу данных."""
    for model in CSV_DICT:
        if model != "Genre_Title":
            model.objects.all().delete()


def read_table(table: str) -> list:
    """Считывает данные из csv и возвращает список строк таблицы."""
    path = f"./static/data/{table}"
    with open(path, encoding="utf-8") as csv_file:
        reader = DictReader(csv_file, delimiter=",")
        return list(reader)


def get_model_fields(model) -> dict:
    """Функция возвращает поля модели."""
    print(type(model))
    fields_list = model._meta.fields
    fields = {field.name: field.attname for field in fields_list}
    return fields


def vet_fields(fields: dict, table: str):
    """Корректирует название полей в таблице."""
    for row in table:
        for field_name in list(row):
            if (
                field_name in fields
                and field_name != fields[field_name.replace("_id", "")]
            ):
                row[fields[field_name]] = row.pop(field_name)


def import_data(model, table: str):
    """
    Сопоставляет имя файла с именем модели
    и загружает данные.
    """
    table = read_table(table)
    vet_fields(get_model_fields(model), table)
    model.objects.bulk_create(model(**row) for row in table)


def import_genre_title():
    """Загружает данные в модель 'genre_title'."""
    table = read_table("genre_title.csv")
    [
        Title.objects.get(id=row["title_id"]).genre.add(row["genre_id"])
        for row in table
    ]


class Command(BaseCommand):
    """
    Импорт данных из csv файлов в базу данных.
    Переходит в директорию, где хранится файл, и сохраняет его.
    """

    help = "Импорт данных из файлов csv в базу данных."

    def add_arguments(self, parser):
        """Добавлен дополнительный ключ для команды."""
        parser.add_argument(
            "-c",
            "--clear",
            action="store_true",
            help="Очищает базу данных."
        )

    def handle(self, *args, **options):
        if options["clear"]:
            db_clear()
            self.stdout.write(
                self.style.SUCCESS("База данных очищена.")
            )
        else:
            for model, table in CSV_DICT.items():
                try:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Импорт из файла {table} в модель {model}..."
                        )
                    )
                    if model == "Genre_Title":
                        import_genre_title()
                    else:
                        import_data(model, table)

                    self.stdout.write(
                        self.style.SUCCESS("Данные успешно загружены.")
                    )
                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Дубликаты полей в {model}, игнорируем..."
                        )
                    )
                    pass
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.ERROR("В локальных файлах нет данных.")
                    )
                except Exception as error:
                    self.stdout.write(self.style.ERROR(
                        "Ошибка загрузки: '%s'" % error)
                    )
