# Generated by Django 4.2.7 on 2023-12-26 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='user_transactions_count',
            field=models.IntegerField(default=0, verbose_name='تراکنش های انجام شده'),
        ),
    ]
