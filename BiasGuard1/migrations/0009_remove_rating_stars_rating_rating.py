# Generated by Django 4.2.4 on 2023-11-21 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BiasGuard1', '0008_rating_remove_offer_qualification_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='stars',
        ),
        migrations.AddField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
