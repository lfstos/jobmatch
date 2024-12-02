# Generated by Django 5.1.3 on 2024-12-02 22:21

import choices.choices
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='nome',
        ),
        migrations.AlterField(
            model_name='empresa',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name='Vaga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_vaga', models.CharField(max_length=100)),
                ('faixa_salarial', models.CharField(choices=choices.choices.get_faixa_salarial_choices, max_length=5)),
                ('escolaridade', models.CharField(choices=choices.choices.get_escolaridade_choices, max_length=18)),
                ('requisitos', models.TextField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresa.empresa')),
            ],
        ),
    ]
