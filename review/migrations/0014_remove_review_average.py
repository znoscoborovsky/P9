# Generated by Django 4.2.3 on 2023-08-07 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0013_rename_time_created_review_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='average',
        ),
    ]