# Generated by Django 3.1.4 on 2021-02-13 19:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wallet_acc', models.FloatField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ordered', 'ordered'), ('paid', 'paid'), ('delivered', 'delivered'), ('rejected', 'rejected')], max_length=20),
        ),
        migrations.DeleteModel(
            name='Notifications',
        ),
        migrations.AddField(
            model_name='wallet',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order'),
        ),
        migrations.AddField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller'),
        ),
    ]