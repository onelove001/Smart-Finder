# Generated by Django 3.1.4 on 2021-03-02 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Added_skills_service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=50)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.service')),
            ],
        ),
    ]
