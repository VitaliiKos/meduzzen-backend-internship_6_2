# Generated by Django 4.2.5 on 2023-10-01 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profilemodel',
            old_name='name',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='profilemodel',
            old_name='surname',
            new_name='phone',
        ),
    ]
