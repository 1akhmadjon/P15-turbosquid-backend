# Generated by Django 4.2.7 on 2023-11-11 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_rename_shoppingcart_shoppingcartt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcartt',
            name='product_id',
            field=models.IntegerField(),
        ),
    ]