# Generated by Django 2.2.8 on 2020-02-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0004_added_block_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
