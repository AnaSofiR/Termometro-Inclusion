# Generated by Django 4.2.4 on 2023-11-12 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BiasGuard1', '0003_offer_recomendation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
