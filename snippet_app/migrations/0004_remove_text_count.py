# Generated by Django 3.2.4 on 2021-06-07 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippet_app', '0003_text_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='count',
        ),
    ]
