# Generated by Django 4.2.7 on 2023-11-11 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_shoppingcart_product_id_shoppingcart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='product_id',
            field=models.IntegerField(default=False),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.IntegerField(default=False),
        ),
    ]