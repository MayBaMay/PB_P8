# Generated by Django 3.0.2 on 2020-02-11 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodSearch', '0005_auto_20200211_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='initial_search_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initial_search_product', to='foodSearch.Product'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='substitute',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='substitute', to='foodSearch.Product'),
        ),
    ]