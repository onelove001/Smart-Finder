# Generated by Django 3.1.4 on 2021-02-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_service_review_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='star_rating',
            name='rating_star',
            field=models.FloatField(),
        ),
    ]