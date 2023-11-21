# Generated by Django 4.2.4 on 2023-11-21 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analitica', '0001_initial'),
        ('BiasGuard1', '0007_remove_offer_qualification_offer_qualification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analitica.candidates')),
            ],
        ),
        migrations.RemoveField(
            model_name='offer',
            name='qualification',
        ),
        migrations.DeleteModel(
            name='qualification',
        ),
        migrations.AddField(
            model_name='rating',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BiasGuard1.offer'),
        ),
    ]