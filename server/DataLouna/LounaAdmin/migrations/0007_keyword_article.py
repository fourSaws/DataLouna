# Generated by Django 4.1.1 on 2022-09-14 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LounaAdmin', '0006_alter_article_options_alter_keywords_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword_Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='LounaAdmin.article', verbose_name='ID Статьи')),
                ('keywords_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='LounaAdmin.keywords', verbose_name='ID Ключевого слова')),
            ],
        ),
    ]
