# Generated by Django 4.2.3 on 2023-08-02 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_vagas", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vagas",
            name="candidatosInscritos",
        ),
        migrations.AlterField(
            model_name="vagas_aplicadas",
            name="vaga",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vagas_aplicadas",
                to="app_vagas.vagas",
            ),
        ),
    ]
