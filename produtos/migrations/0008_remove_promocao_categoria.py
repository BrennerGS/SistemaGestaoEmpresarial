# Generated by Django 5.0.3 on 2024-09-23 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0007_alter_userprofile_imagem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promocao',
            name='Categoria',
        ),
    ]
