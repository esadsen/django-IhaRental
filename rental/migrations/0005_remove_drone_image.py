# Generated by Django 5.0.2 on 2024-07-17 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0004_alter_drone_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drone',
            name='image',
        ),
    ]
