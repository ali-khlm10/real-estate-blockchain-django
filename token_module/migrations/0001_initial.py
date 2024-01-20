# Generated by Django 4.2.7 on 2024-01-20 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='smartContractModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_name', models.CharField(max_length=250, verbose_name='نام قرارداد هوشمند')),
                ('contract_address', models.CharField(editable=False, max_length=2000, verbose_name='آدرس قرارداد هوشمند')),
                ('contract_inventory', models.FloatField(default=0.0, verbose_name='موجودی قرارداد هوشمند')),
                ('nonce', models.IntegerField(default=0, verbose_name='تعداد دفعات فراخوانی')),
            ],
            options={
                'verbose_name': 'قرارداد هوشمند',
                'verbose_name_plural': 'قراردادهای هوشمند',
            },
        ),
        migrations.CreateModel(
            name='propertyTokenModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_owner_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس مالک توکن')),
                ('token_id', models.CharField(max_length=500, unique=True, verbose_name='شماره توکن ملک')),
                ('token_created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ایجاد توکن')),
                ('is_published', models.BooleanField(default=False, verbose_name='منتشر شده/نشده')),
                ('token_information', models.TextField(blank=True, null=True, verbose_name='اطلاعات مربوط به توکن')),
                ('property_of_token', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_of_token', to='property_module.propertymodel', verbose_name='ملک مربوط به توکن')),
            ],
            options={
                'verbose_name': 'توکن',
                'verbose_name_plural': 'توکن ها',
            },
        ),
    ]
