# Generated by Django 5.1.1 on 2024-10-03 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_service', '0002_alter_payment_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='session_url',
            field=models.TextField(),
        ),
    ]
