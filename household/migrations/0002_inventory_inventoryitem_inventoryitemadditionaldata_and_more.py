# Generated by Django 5.1.5 on 2025-02-04 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('household', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='household.household')),
            ],
            options={
                'verbose_name_plural': 'Pantries',
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_type', models.CharField(choices=[('pantry', 'Pantry'), ('storeroom', 'Storeroom'), ('private', 'Private')], max_length=20)),
                ('item_name', models.CharField(max_length=100, unique=True)),
                ('generic_name', models.CharField(default='', max_length=100)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(choices=[('g', 'Grams'), ('ml', 'Milliliters'), ('pcs', 'Pieces')], max_length=10)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.inventory')),
            ],
            options={
                'verbose_name_plural': 'Pantry Items',
            },
        ),
        migrations.CreateModel(
            name='InventoryItemAdditionalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='household.inventoryitem')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItemPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(choices=[('g', 'Grams'), ('ml', 'Milliliters'), ('pcs', 'Pieces')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_purchased', models.DateField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.inventoryitem')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPurchaseAdditionalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('purchase', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='household.inventoryitempurchase')),
            ],
        ),
    ]
