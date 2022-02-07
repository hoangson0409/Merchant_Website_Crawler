from django.contrib import admin
from . import models
from . import forms
from .csvexport import actions
from django.utils.html import format_html


# Register your models here.
class InputPeterAdmin(admin.ModelAdmin):
    form = forms.InputPeterForm
    model = models.InputPeter
    readonly_fields = ['input_id', 'timestamp', 'task_id', ]
    list_display = ('__str__', 'timestamp', 'domain', 'keywords', 'keyword_logic')
    list_filter = ['domain', 'keywords', 'keyword_logic']
    search_fields = ('domain', 'keywords', 'keyword_logic', 'input_id')
    date_hierarchy = 'ts'

    # Adding csv export action
    actions = [actions.csvexport]

    # Display Name different from db name
    @admin.display(description='timestamp')
    def timestamp(self, obj):
        return obj.ts


class OutputPeterAdmin(admin.ModelAdmin):
    model = models.OutputPeter
    readonly_fields = ['output_id', 'input_id', 'scan_url', 'scan_time',
                       'page_content', 'response_code', 'reason', 'keyword_matched',
                       'screenshot_dir', 'image_tag']
    list_display = ('__str__', 'input_id', 'scan_time', 'scan_url',
                    'response_code', 'reason', 'keyword_matched')
    list_filter = ['response_code', 'reason', 'keyword_matched']
    search_fields = ('page_content', 'url', 'response_code', 'reason')
    exclude = ('url',)
    date_hierarchy = 'scan_time'
    actions = [actions.csvexport]

    @admin.display(description='Screenshot')
    def image_tag(self, obj):
        return format_html('<img src="/static/{}" />'.format(obj.screenshot_dir))

    @admin.display(description='scan url')
    def scan_url(self, obj):
        return obj.url


class InputMaryAdmin(admin.ModelAdmin):
    form = forms.InputMaryForm
    model = models.InputMary
    readonly_fields = ['input_id', 'timestamp', 'task_id', ]
    list_display = ('__str__', 'timestamp', 'run_type',
                    'pw_product', 'merchant_id', 'merchant_name',
                    'project_id', 'project_name', 'keywords', 'keyword_logic')
    list_filter = ['run_type', 'pw_product',
                   'merchant_id', 'merchant_name',
                   'project_id', 'project_name', ]
    search_fields = ('input_id', 'pw_product',
                     'merchant_id', 'merchant_name',
                     'project_id', 'project_name')
    date_hierarchy = 'ts'
    actions = [actions.csvexport]

    # Display Name different from db name
    @admin.display(description='timestamp')
    def timestamp(self, obj):
        return obj.ts


class OutputMaryAdmin(admin.ModelAdmin):
    model = models.OutputMary
    readonly_fields = ['output_id', 'input_id',
                       'scan_time', 'pw_product',
                       'merchant_id', 'merchant_name',
                       'project_id', 'project_name',
                       'merchant_url', 'scan_url',
                       'page_content', 'scheduled_counter',
                       'response_code', 'reason', 'keyword_matched',
                       'screenshot_dir', 'image_tag']
    list_display = ('__str__', 'pw_product',
                    'merchant_id', 'merchant_name',
                    'project_id', 'project_name',
                    'merchant_url', 'scan_url',
                    'scheduled_counter', 'response_code', 'reason',
                    'keyword_matched', 'input_id')
    list_filter = ['pw_product', 'merchant_id', 'merchant_name',
                   'project_id', 'project_name',
                   'response_code', 'reason', 'keyword_matched']
    search_fields = ('page_content', 'pw_product', 'merchant_id', 'merchant_name',
                     'project_id', 'project_name', 'input_id__input_id',
                     'response_code', 'reason')
    exclude = ('url',)
    date_hierarchy = 'scan_time'
    actions = [actions.csvexport]

    @admin.display(description='Screenshot')
    def image_tag(self, obj):
        return format_html('<img src="/static/{}" />'.format(obj.screenshot_dir))

    @admin.display(description='scan url')
    def scan_url(self, obj):
        return obj.url


admin.site.register(models.InputPeter, InputPeterAdmin)
admin.site.register(models.OutputPeter, OutputPeterAdmin)
admin.site.register(models.InputMary, InputMaryAdmin)
admin.site.register(models.OutputMary, OutputMaryAdmin)
