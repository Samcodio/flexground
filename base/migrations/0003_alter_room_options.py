# Generated by Django 4.2.7 on 2023-11-27 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_message_room_topic_delete_project_room_topic_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
