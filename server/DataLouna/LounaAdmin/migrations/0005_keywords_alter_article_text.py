# Generated by Django 4.1.1 on 2022-09-14 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LounaAdmin', '0004_article_photo_alter_article_text_alter_article_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(),
        ),
    ]
