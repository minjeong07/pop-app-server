# Generated by Django 4.0.3 on 2022-03-17 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_message_left_message_top'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='from_user',
        ),
    ]
