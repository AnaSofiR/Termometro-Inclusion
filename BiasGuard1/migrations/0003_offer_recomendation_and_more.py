# Generated by Django 4.2.4 on 2023-11-12 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analitica', '0001_initial'),
        ('BiasGuard1', '0002_candidates_description_discrimination_qualification_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='offer',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('salary', models.FloatField()),
                ('education_level', models.CharField(max_length=45)),
                ('city', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='recomendation',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='description',
            name='discrimination',
        ),
        migrations.RemoveField(
            model_name='requirements',
            name='vacant',
        ),
        migrations.RemoveField(
            model_name='vacants',
            name='company',
        ),
        migrations.RemoveField(
            model_name='vacants',
            name='description',
        ),
        migrations.RemoveField(
            model_name='vacants',
            name='qualification',
        ),
        migrations.RemoveField(
            model_name='discrimination',
            name='alert',
        ),
        migrations.RemoveField(
            model_name='discrimination',
            name='discrimination_name',
        ),
        migrations.RemoveField(
            model_name='discrimination',
            name='percetage',
        ),
        migrations.RemoveField(
            model_name='discrimination',
            name='recommendation',
        ),
        migrations.AddField(
            model_name='discrimination',
            name='type',
            field=models.CharField(default='Sin discriminación', max_length=45),
        ),
        migrations.AlterField(
            model_name='discrimination',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analitica.candidates'),
        ),
        migrations.DeleteModel(
            name='candidates',
        ),
        migrations.DeleteModel(
            name='companies',
        ),
        migrations.DeleteModel(
            name='description',
        ),
        migrations.DeleteModel(
            name='requirements',
        ),
        migrations.DeleteModel(
            name='vacants',
        ),
        migrations.AddField(
            model_name='offer',
            name='discrimination',
            field=models.ManyToManyField(to='BiasGuard1.discrimination'),
        ),
        migrations.AddField(
            model_name='offer',
            name='qualification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BiasGuard1.qualification'),
        ),
        migrations.AddField(
            model_name='discrimination',
            name='recomendation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='BiasGuard1.recomendation'),
        ),
    ]
