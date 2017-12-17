# Generated by Django 2.0 on 2017-12-17 01:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('nothotdog', '0004_auto_20171217_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='computed_status',
            field=models.PositiveSmallIntegerField(
                choices=[(0, 'pending'), (1, 'in progress'), (2, 'completed'), (2, 'error'), (4, 'force')],
                default=None, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set(),
        ),
    ]
