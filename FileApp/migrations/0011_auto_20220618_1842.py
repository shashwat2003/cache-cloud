# Generated by Django 2.1.5 on 2022-06-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileApp', '0010_auto_20220617_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='size',
            field=models.BigIntegerField(),
        ),
    ]
