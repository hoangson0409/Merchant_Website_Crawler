# Generated by Django 3.2.5 on 2021-08-01 04:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210801_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputpeter',
            name='domain_id',
            field=models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='main.inputpeter'),
        ),
    ]