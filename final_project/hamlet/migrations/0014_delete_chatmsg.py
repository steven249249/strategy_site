# Generated by Django 3.2.13 on 2022-06-12 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hamlet', '0013_chatmsg'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChatMsg',
        ),
    ]