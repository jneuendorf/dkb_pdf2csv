# Generated by Django 3.1.1 on 2020-09-20 20:11

import data_vis.models.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_vis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdfFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pdfs/%Y/', validators=[data_vis.models.validators.validate_is_pdf])),
                ('imported', models.BooleanField(default=False)),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pdfs', to='data_vis.series')),
            ],
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
