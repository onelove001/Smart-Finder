# Generated by Django 3.1.4 on 2021-02-27 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_thread_chatt'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='chatt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_chat', to='chat.chatmessage'),
        ),
    ]