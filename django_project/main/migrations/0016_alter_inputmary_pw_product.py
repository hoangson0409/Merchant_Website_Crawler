# Generated by Django 3.2.5 on 2021-08-02 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20210802_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputmary',
            name='pw_product',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
