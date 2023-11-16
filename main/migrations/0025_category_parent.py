# Generated by Django 4.2.7 on 2023-11-16 12:02

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_category_options_remove_sections_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='main.category'),
        ),
    ]