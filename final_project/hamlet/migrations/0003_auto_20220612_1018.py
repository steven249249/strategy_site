# Generated by Django 3.2.12 on 2022-06-12 02:18

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hamlet', '0002_auto_20220610_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='inform',
            name='pub_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]