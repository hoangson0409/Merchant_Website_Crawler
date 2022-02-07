from django.db import models
import uuid


class InputPeter(models.Model):
    input_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    domain = models.CharField(max_length=100, unique=False)
    ts = models.DateTimeField(auto_now=True, db_index=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    keyword_logic = models.CharField(max_length=3, null=True, blank=True)
    task_id = models.UUIDField(null=True, unique=True)
    # run_type = models.CharField(max_length=10, null=True, blank=True)


class OutputPeter(models.Model):
    output_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    input_id = models.ForeignKey(InputPeter, on_delete=models.CASCADE, default=uuid.uuid4, db_column='input_id')
    url = models.URLField(unique=False, null=True)
    scan_time = models.DateTimeField(auto_now=True, db_index=True)
    response_code = models.PositiveIntegerField(null=True, blank=True)
    page_content = models.TextField(null=True)
    screenshot_dir = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(null=True)
    keyword_matched = models.PositiveIntegerField(default=0)


class InputMary(models.Model):
    input_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ts = models.DateTimeField(auto_now=True, db_index=True)
    pw_product = models.CharField(max_length=25, null=True, blank=True)
    merchant_id = models.PositiveIntegerField(blank=True, null=True)
    merchant_name = models.CharField(max_length=255, null=True, blank=True)
    project_id = models.PositiveIntegerField(blank=True, null=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    keyword_logic = models.CharField(max_length=3, null=True, blank=True)
    task_id = models.UUIDField(null=True, unique=True)
    run_type = models.CharField(max_length=10, null=True, blank=True)


class OutputMary(models.Model):
    output_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    input_id = models.ForeignKey(InputMary, on_delete=models.CASCADE, default=uuid.uuid4, db_column='input_id')
    url = models.URLField(unique=False, null=True)
    merchant_url = models.CharField(max_length=255, null=True, blank=True)
    pw_product = models.CharField(max_length=25, blank=True, null=True)
    merchant_id = models.PositiveIntegerField(blank=True, null=True)
    merchant_name = models.CharField(max_length=255, null=True, blank=True)
    project_id = models.PositiveIntegerField(blank=True, null=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    scan_time = models.DateTimeField(auto_now=True, db_index=True)
    response_code = models.PositiveIntegerField(null=True, blank=True)
    page_content = models.TextField(null=True)
    screenshot_dir = models.CharField(max_length=255, null=True, blank=True)
    scheduled_counter = models.PositiveIntegerField(null=True, blank=True)
    reason = models.TextField(null=True)
    keyword_matched = models.PositiveIntegerField(default=0)

# TODO: Database Routers
