# Generated by Django 3.1.4 on 2021-02-03 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_reviews_service_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='review_key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.reviews'),
        ),
    ]
