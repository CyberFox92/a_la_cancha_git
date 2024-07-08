# Generated by Django 5.0.6 on 2024-06-07 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_alquiler', '0008_alter_usuario_celular'),
    ]

    operations = [
        # Agregar la columna celular a la tabla auth_user
        migrations.RunSQL('''
            ALTER TABLE auth_user
            ADD COLUMN celular varchar(20);
        '''),
    ]
