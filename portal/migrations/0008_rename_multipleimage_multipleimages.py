# Generated by Django 4.2 on 2023-05-10 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_multipleimage_delete_multipleimages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MultipleImage',
            new_name='MultipleImages',
        ),
    ]