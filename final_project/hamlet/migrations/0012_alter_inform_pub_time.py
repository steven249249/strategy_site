# Generated by Django 3.2.13 on 2022-06-11 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hamlet', '0011_alter_inform_pub_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inform',
            name='pub_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]