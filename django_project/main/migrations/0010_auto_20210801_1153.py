# Generated by Django 3.2.5 on 2021-08-01 04:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_outputpeter_domain_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessrecord',
            name='domain_id',
            field=models.ForeignKey(db_column='domain_id', default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='main.searchdomain'),
        ),
        migrations.AlterField(
            model_name='outputpeter',
            name='domain_id',
            field=models.ForeignKey(db_column='domain_id', default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='main.inputpeter'),
        ),
    ]