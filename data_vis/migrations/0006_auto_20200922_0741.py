# Generated by Django 3.1.1 on 2020-09-22 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_vis', '0005_auto_20200922_0608'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='datapoint',
            unique_together={('series', 'x', 'dy', 'meta')},
        ),
    ]
