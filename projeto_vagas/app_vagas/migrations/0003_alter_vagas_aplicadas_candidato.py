# Generated by Django 4.2.3 on 2023-08-02 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_vagas', '0002_remove_vagas_candidatosinscritos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vagas_aplicadas',
            name='candidato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidatos_aplicados', to='app_vagas.candidato'),
        ),
    ]