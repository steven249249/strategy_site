# Generated by Django 3.2.13 on 2022-06-12 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMsg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('msg', models.CharField(max_length=1000)),
                ('board', models.CharField(max_length=100)),
                ('send_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'hamlet_chatmsg',
            },
        ),
    ]
