# Generated by Django 3.0.2 on 2020-01-18 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodSearch', '0004_auto_20200118_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='nb_products',
        ),
        migrations.RemoveField(
            model_name='category',
            name='url',
        ),
    ]
