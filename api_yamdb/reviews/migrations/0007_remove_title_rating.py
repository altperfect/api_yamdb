# Generated by Django 3.2 on 2023-02-17 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_category_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]