# Generated by Django 4.1.1 on 2022-09-14 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LounaAdmin', '0008_alter_categorynode_articles_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorynode',
            name='articles',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='Статьи',
                to='LounaAdmin.article',
            ),
        ),
        migrations.AlterField(
            model_name='categorynode',
            name='children',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='Ребенок',
                to='LounaAdmin.categorynode',
            ),
        ),
        migrations.AlterField(
            model_name='categorynode',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='Родитель',
                to='LounaAdmin.categorynode',
            ),
        ),
    ]
