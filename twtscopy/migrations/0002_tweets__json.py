# Generated by Django 2.2.1 on 2019-05-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twtscopy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweets',
            name='_json',
            field=models.TextField(default='{}'),
        ),
    ]
