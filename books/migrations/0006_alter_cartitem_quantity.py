# Generated by Django 4.2.4 on 2023-08-12 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
