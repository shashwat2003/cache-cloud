# Generated by Django 2.1.5 on 2022-06-16 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FileApp', '0005_auto_20220616_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='mimetype',
        ),
        migrations.AddField(
            model_name='file',
            name='catogery',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='FileApp.Catogery'),
        ),
    ]
