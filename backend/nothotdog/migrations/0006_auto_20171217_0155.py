# Generated by Django 2.0 on 2017-12-17 01:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('nothotdog', '0005_auto_20171217_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
