# Generated by Django 3.2.13 on 2022-06-11 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hamlet', '0005_alter_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='inform',
            name='pub_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
