# Generated by Django 3.2.13 on 2022-06-10 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hamlet', '0003_remove_user_login_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]