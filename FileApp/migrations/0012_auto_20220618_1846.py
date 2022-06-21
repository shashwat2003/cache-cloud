# Generated by Django 2.1.5 on 2022-06-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileApp', '0011_auto_20220618_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='deleted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='file',
            name='expiry',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]