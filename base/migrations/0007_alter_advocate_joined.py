# Generated by Django 4.1.4 on 2023-01-19 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_advocate_followers_advocate_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advocate',
            name='joined',
            field=models.DateField(blank=True, null=True),
        ),
    ]
