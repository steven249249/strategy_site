# Generated by Django 3.2.13 on 2022-06-11 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hamlet', '0008_inform_pub_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inform',
            name='pub_time',
        ),
    ]