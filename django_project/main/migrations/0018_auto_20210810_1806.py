# Generated by Django 3.2.5 on 2021-08-10 11:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210802_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inputpeter',
            old_name='domain_id',
            new_name='input_id',
        ),
        migrations.RenameField(
            model_name='outputmary',
            old_name='url_id',
            new_name='output_id',
        ),
        migrations.RenameField(
            model_name='outputpeter',
            old_name='url_id',
            new_name='output_id',
        ),
        migrations.RemoveField(
            model_name='outputpeter',
            name='domain_id',
        ),
        migrations.AddField(
            model_name='inputmary',
            name='keyword_logic',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='inputmary',
            name='keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inputmary',
            name='project_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inputmary',
            name='project_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inputmary',
            name='run_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='inputpeter',
            name='keyword_logic',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='outputmary',
            name='keyword_matched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='outputmary',
            name='project_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outputmary',
            name='project_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='outputmary',
            name='reason',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='outputmary',
            name='scheduled_counter',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outputpeter',
            name='input_id',
            field=models.ForeignKey(db_column='input_id', default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='main.inputpeter'),
        ),
        migrations.AddField(
            model_name='outputpeter',
            name='keyword_matched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='outputpeter',
            name='reason',
            field=models.TextField(null=True),
        ),
    ]
