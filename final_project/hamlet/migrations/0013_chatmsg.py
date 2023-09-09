# Generated by Django 3.2.13 on 2022-06-12 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hamlet', '0012_alter_inform_pub_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMsg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=1000)),
                ('send_time', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hamlet.board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hamlet.user')),
            ],
        ),
    ]