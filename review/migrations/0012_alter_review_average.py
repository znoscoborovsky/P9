# Generated by Django 4.2.3 on 2023-08-01 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0011_review_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='average',
            field=models.JSONField(blank=True),
        ),
    ]