# Generated by Django 3.1.1 on 2020-09-26 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_vis', '0009_auto_20200925_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='is_abstract',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
