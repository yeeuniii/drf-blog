# Generated by Django 5.0.1 on 2024-01-30 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_alter_post_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='password',
            field=models.CharField(default='0000', max_length=4),
        ),
    ]
