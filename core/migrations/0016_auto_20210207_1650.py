# Generated by Django 3.1.4 on 2021-02-07 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210207_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requests',
            old_name='employer',
            new_name='poster',
        ),
    ]
