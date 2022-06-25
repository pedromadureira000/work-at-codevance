# Generated by Django 4.0.5 on 2022-06-25 00:00

from django.db import migrations, models
import django_cpf_cnpj.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=60, verbose_name='company name')),
                ('cnpj', django_cpf_cnpj.fields.CNPJField(max_length=18, verbose_name='CNPJ')),
            ],
            options={
                'verbose_name': 'supplier company',
                'verbose_name_plural': 'supplier companies',
                'default_permissions': [],
            },
        ),
    ]