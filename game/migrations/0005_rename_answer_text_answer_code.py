# Generated by Django 4.2.13 on 2024-07-03 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_alter_answer_code_lang'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='answer_text',
            new_name='code',
        ),
    ]
