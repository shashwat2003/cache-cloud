# Generated by Django 2.1.5 on 2022-06-16 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FileApp', '0002_catogery'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiMeType',
            fields=[
                ('type', models.CharField(max_length=125, primary_key=True, serialize=False)),
                ('catogery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FileApp.Catogery')),
            ],
        ),
    ]
