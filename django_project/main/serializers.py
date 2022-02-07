from rest_framework import serializers
from .models import OutputPeter, InputPeter, OutputMary, InputMary


class OutputPeterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OutputPeter
        fields = ('output_id', 'url', 'scan_time', 'input_id',
                  'response_code', 'page_content', 'screenshot_dir', 'reason')


class InputPeterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InputPeter
        fields = ('input_id', 'task_id', 'domain',
                  'keywords', 'ts', 'keyword_logic')


class OutputMarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OutputMary
        fields = ('output_id', 'url', 'merchant_url', 'pw_product',
                  'merchant_id', 'merchant_name', 'project_id',
                  'project_name', 'scan_time', 'input_id',
                  'scheduled_counter', 'response_code',
                  'page_content', 'screenshot_dir', 'reason')


class InputMarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InputMary
        fields = ('input_id', 'ts', 'pw_product', 'merchant_id',
                  'merchant_name', 'project_id', 'project_name',
                  'keywords', 'keyword_logic', 'run_type', 'task_id')
