# Generated by Django 3.1.4 on 2021-02-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210206_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='ordered',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ordered', 'ordered'), ('delivered', 'delivered'), ('rejected', 'rejected')], max_length=20),
        ),
    ]
