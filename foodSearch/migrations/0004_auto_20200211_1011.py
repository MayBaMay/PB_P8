# Generated by Django 3.0.2 on 2020-02-11 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodSearch', '0003_auto_20200210_1918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='product',
            new_name='substitute',
        ),
    ]