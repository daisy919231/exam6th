# Generated by Django 5.1 on 2024-08-21 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_rename_category_attribute_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='product.product'),
        ),
    ]
