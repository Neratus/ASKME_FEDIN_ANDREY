# Generated by Django 4.2.16 on 2024-12-16 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_rename_user_answer_author_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="is_correct",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="answerlike",
            name="type",
            field=models.CharField(
                choices=[("like", "Like"), ("dislike", "Dislike")],
                default="like",
                max_length=7,
            ),
        ),
        migrations.AddField(
            model_name="questionlike",
            name="type",
            field=models.CharField(
                choices=[("like", "Like"), ("dislike", "Dislike")],
                default="like",
                max_length=7,
            ),
        ),
    ]
