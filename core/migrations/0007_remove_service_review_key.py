# Generated by Django 3.1.4 on 2021-02-03 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_service_review_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='review_key',
        ),
    ]