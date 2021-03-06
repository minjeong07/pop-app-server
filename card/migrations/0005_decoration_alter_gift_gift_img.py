# Generated by Django 4.0.3 on 2022-03-21 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_message_author_message_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deco_name', models.CharField(max_length=200)),
                ('deco_img', models.ImageField(upload_to='deco/')),
            ],
            options={
                'db_table': 'decoration',
            },
        ),
        migrations.AlterField(
            model_name='gift',
            name='gift_img',
            field=models.ImageField(upload_to='gift/'),
        ),
    ]
