# Generated by Django 5.0.1 on 2024-02-01 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_rename_posting_id_comment_post_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]
