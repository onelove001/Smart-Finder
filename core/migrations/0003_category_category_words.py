# Generated by Django 3.1.4 on 2021-02-10 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contact_us'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_words',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]