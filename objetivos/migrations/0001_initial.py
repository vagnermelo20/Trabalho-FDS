# Generated by Django 5.1.7 on 2025-04-03 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=1000)),
                ('Descrição', models.TextField()),
                ('Estar_concluído', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=100, unique=True)),
                ('E_mail', models.EmailField(max_length=254, unique=True)),
                ('Senha', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subtarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=255)),
                ('descrição', models.TextField()),
                ('estar_concluído', models.BooleanField(default=False)),
                ('objetivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Subtarefas', to='objetivos.objetivo')),
            ],
        ),
        migrations.AddField(
            model_name='objetivo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Objetivos', to='objetivos.usuario'),
        ),
    ]
