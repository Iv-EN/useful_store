# Generated by Django 5.1.4 on 2025-01-11 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="number_views",
            field=models.IntegerField(
                default=0, verbose_name="количество просмотров"
            ),
        ),
    ]