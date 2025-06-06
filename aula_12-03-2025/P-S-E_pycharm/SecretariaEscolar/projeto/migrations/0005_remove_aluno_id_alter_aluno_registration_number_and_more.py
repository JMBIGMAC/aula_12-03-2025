# Generated by Django 5.1.8 on 2025-04-09 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projeto", "0004_remove_aluno_first_name_aluno_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aluno",
            name="id",
        ),
        migrations.AlterField(
            model_name="aluno",
            name="registration_number",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="Número de Registro"
            ),
        ),
        migrations.AlterField(
            model_name="contrato",
            name="email_responsavel",
            field=models.EmailField(
                blank=True,
                max_length=254,
                null=True,
                verbose_name="Email do Responsável",
            ),
        ),
        migrations.AlterField(
            model_name="contrato",
            name="responsavel",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="projeto.responsavel",
                verbose_name="Nome do Responsável",
            ),
        ),
    ]
