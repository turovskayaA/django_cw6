# Generated by Django 5.0.4 on 2024-04-21 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_message_newsletter_logi'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='client',
            field=models.ManyToManyField(related_name='letter', to='client.serviceclient'),
        ),
    ]
