# Generated by Django 4.2 on 2023-05-10 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_multipleindimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multipleindimage',
            name='images',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
