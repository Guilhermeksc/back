# Generated by Django 5.1.4 on 2025-01-13 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_planejamento', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='controleprocessos',
            old_name='uasg',
            new_name='unidade_compra',
        ),
        migrations.AlterModelTable(
            name='controleprocessos',
            table='app_planejamento_controleprocessos',
        ),
    ]
