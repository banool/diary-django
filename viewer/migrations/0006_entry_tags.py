# Generated by Django 2.0.3 on 2018-08-20 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0005_auto_20180328_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.CharField(default='', max_length=200),
        ),
    ]
