# Generated by Django 4.1.1 on 2022-10-26 01:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LounaAdmin", "0013_alter_inactivenewstellers_after_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inactivenewstellers",
            name="after_time",
            field=models.IntegerField(verbose_name="Отправить через "),
        ),
        migrations.AlterField(
            model_name="user",
            name="registration_date",
            field=models.DateField(
                default=datetime.datetime(2022, 10, 26, 1, 9, 1, 556545),
                verbose_name="Дата регистрации",
            ),
        ),
    ]
