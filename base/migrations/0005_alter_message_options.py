# Generated by Django 5.0.3 on 2024-04-17 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
