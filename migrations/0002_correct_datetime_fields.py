# Generated by Django 2.2.1 on 2019-07-01 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='block',
            options={'ordering': ['-start']},
        ),
        migrations.AlterModelOptions(
            name='workcategory',
            options={'ordering': ['name'], 'verbose_name_plural': 'work categories'},
        ),
        migrations.AlterField(
            model_name='block',
            name='end',
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='start',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='workcategory',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
