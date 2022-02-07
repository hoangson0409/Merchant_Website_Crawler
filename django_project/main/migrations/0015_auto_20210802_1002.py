# Generated by Django 3.2.5 on 2021-08-02 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210802_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='outputmary',
            name='merchant_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outputmary',
            name='merchant_name',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outputmary',
            name='pw_product',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
