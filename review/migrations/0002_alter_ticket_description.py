# Generated by Django 4.2.3 on 2023-07-18 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.CharField(blank=True, max_length=2048, verbose_name='description'),
        ),
    ]
