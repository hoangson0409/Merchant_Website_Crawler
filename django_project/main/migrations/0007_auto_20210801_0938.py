# Generated by Django 3.2.5 on 2021-08-01 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210801_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accessrecord',
            name='timezone',
        ),
        migrations.AlterField(
            model_name='accessrecord',
            name='domain_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
