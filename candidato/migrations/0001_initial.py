# Generated by Django 5.1.3 on 2024-12-03 21:50

import choices.choices
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresa', '0002_remove_empresa_nome_alter_empresa_email_vaga'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faixa_salarial', models.CharField(choices=choices.choices.get_faixa_salarial_choices, max_length=5)),
                ('escolaridade', models.CharField(choices=choices.choices.get_escolaridade_choices, max_length=18)),
                ('experiencia', models.TextField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING,
                                            to=settings.AUTH_USER_MODEL)),
                ('vagas', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresa.vaga')),
            ],
        ),
    ]
