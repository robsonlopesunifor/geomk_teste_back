# Generated by Django 2.2.7 on 2019-11-13 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='time',
            field=models.CharField(default='', max_length=100),
        ),
    ]
