# Generated by Django 2.2 on 2021-03-18 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20210318_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт'),
        ),
    ]
