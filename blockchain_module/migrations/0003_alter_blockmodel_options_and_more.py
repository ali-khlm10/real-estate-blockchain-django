# Generated by Django 4.2.7 on 2023-12-17 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain_module', '0002_alter_transactionstatusmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blockmodel',
            options={'verbose_name': 'بلاک', 'verbose_name_plural': 'بلاک ها'},
        ),
        migrations.AlterModelOptions(
            name='transactionsmodel',
            options={'verbose_name': 'تراکنش', 'verbose_name_plural': 'تراکنش ها'},
        ),
        migrations.AlterModelOptions(
            name='transactionstatusmodel',
            options={'verbose_name': 'وضعیت تراکنش', 'verbose_name_plural': 'وضعیت تراکنش ها'},
        ),
    ]
