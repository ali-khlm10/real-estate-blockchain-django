# Generated by Django 4.2.7 on 2023-12-24 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_module', '0004_alter_nodemodel_node_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodemodel',
            name='is_disable',
            field=models.BooleanField(default=True, verbose_name='فعال/غیرفعال'),
        ),
    ]
