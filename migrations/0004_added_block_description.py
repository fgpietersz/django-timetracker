# Generated by Django 2.2.3 on 2019-08-14 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0003_unique_indices_name_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='end',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]