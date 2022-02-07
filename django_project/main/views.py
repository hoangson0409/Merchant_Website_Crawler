import os

from .forms import InputPeterForm, InputMaryForm
from .models import OutputPeter, InputPeter, OutputMary, InputMary
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from rest_framework import viewsets
from .serializers import OutputPeterSerializer, InputPeterSerializer, OutputMarySerializer, InputMarySerializer
from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI(os.getenv('PW_SCRAPY_URL', 'http://localhost:6800'))


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False
    return True


# MAIN PAGE
def spiderman(request):
    return render(request, 'spiderman.html', context={})


# class for RESTAPI
class OutputPeterViewSet(viewsets.ModelViewSet):
    # ModelViewSet is a special view that Django Rest Framework provides. It will handle GET and POST for Django Item
    queryset = OutputPeter.objects.all()  # .order_by('scan_time')
    serializer_class = OutputPeterSerializer


class InputPeterViewSet(viewsets.ModelViewSet):
    # ModelViewSet is a special view that Django Rest Framework provides. It will handle GET and POST for Django Item
    queryset = InputPeter.objects.all()  # .order_by('scan_time')
    serializer_class = InputPeterSerializer


class OutputMaryViewSet(viewsets.ModelViewSet):
    # ModelViewSet is a special view that Django Rest Framework provides. It will handle GET and POST for Django Item
    queryset = OutputMary.objects.all()  # .order_by('scan_time')
    serializer_class = OutputMarySerializer


class InputMaryViewSet(viewsets.ModelViewSet):
    # ModelViewSet is a special view that Django Rest Framework provides. It will handle GET and POST for Django Item
    queryset = InputMary.objects.all()  # .order_by('scan_time')
    serializer_class = InputMarySerializer


### ModelForms
def peter_parker(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InputPeterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()  # Simplified due to ModelForm
            # redirect to a new URL:
            # return HttpResponseRedirect('/main/crawl_result')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = InputPeterForm()

    return render(request, 'peter_parker.html', {'form': form})


# @csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def peter_parker_crawl(request):
    if request.method == 'POST':
        form = InputPeterForm(request.POST)
        form.save()
        input_id = str(request.POST.get('input_id', None))
        input_id_new = input_id.replace('-', '')
        # header_settings = {
        #     'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        # }
        scrapyd_project = os.getenv('PW_SCRAPY_PROJECT', 'spiderman')
        scrapyd_spider = os.getenv('PW_SCRAPY_SPIDER', 'peter_parker')
        task = scrapyd.schedule(scrapyd_project,
                                scrapyd_spider,
                                # settings=header_settings,
                                input_id=input_id_new,
                                )
        InputPeter.objects.filter(input_id=input_id).update(task_id=task)

        return HttpResponseRedirect('/main/crawl_result1/')
        # return JsonResponse({'task_id': task, 'domain': domain, 'domain_id': domain_id,
        #                      'status': 'started'})
    elif request.method == 'GET':
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get('task_id', None)
        if not task_id:
            return JsonResponse({'error': 'Missing args'})
        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('scrapy_app', task_id)
        if status == 'finished':
            try:
                item = OutputPeter.objects.get(task_id=task_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})


class peter_output(ListView):
    queryset = OutputPeter.objects.select_related('input_id').filter(keyword_matched=1).order_by('-scan_time')
    template_name = 'crawl_result.html'
    paginate_by = 10


def peter_output_detail(request, output_id):
    outputpeter = OutputPeter.objects.select_related('input_id').get(pk=output_id)
    return render(request, 'crawl_result_detail.html', {
        "output_id": outputpeter.output_id,
        "search_term": outputpeter.input_id.domain + ' ' + outputpeter.input_id.keywords,
        "url": outputpeter.url,
        "scan_time": outputpeter.scan_time,
        "page_content": outputpeter.page_content,
        "screenshot_dir": outputpeter.screenshot_dir,
    })


def mary_janes(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InputMaryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            # return HttpResponseRedirect('/main/crawl_result')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = InputMaryForm()
    return render(request, 'mary_janes.html', {'form': form})


@require_http_methods(['POST', 'GET'])  # only get and post
def mary_janes_crawl(request):
    if request.method == 'POST':
        form = InputMaryForm(request.POST)
        form.save()
        run_type = request.POST.get('run_type')
        input_id = str(request.POST.get('input_id', None))
        input_id_new = input_id.replace('-', '')

        if run_type == 'one_time':
            # header_settings = {
            #     'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            # }
            scrapyd_project = os.getenv('PW_SCRAPY_PROJECT', 'spiderman')
            scrapyd_spider = os.getenv('PW_SCRAPY_SPIDER', 'mary_janes')
            task = scrapyd.schedule(scrapyd_project,
                                    scrapyd_spider,
                                    # settings=header_settings,
                                    input_id=input_id_new,
                                    )
            InputMary.objects.filter(input_id=input_id).update(task_id=task)

            return HttpResponseRedirect('/main/crawl_result2/')
            # return JsonResponse({'task_id': task, 'domain': domain, 'input_id': input_id,
            #                      'status': 'started'})
        else:
            return JsonResponse({'run_type': run_type,
                                 'id_for_argument': input_id_new})
    elif request.method == 'GET':
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get('task_id', None)
        if not task_id:
            return JsonResponse({'error': 'Missing args'})
        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('scrapy_app', task_id)
        if status == 'finished':
            try:
                item = OutputMary.objects.get(task_id=task_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})


class mary_output(ListView):
    queryset = OutputMary.objects.select_related('input_id').filter(keyword_matched=1).order_by('-scan_time')
    template_name = 'crawl_result2.html'
    paginate_by = 10


def mary_output_detail(request, output_id):
    outputmary = OutputMary.objects.select_related('input_id').get(pk=output_id)
    return render(request, 'crawl_result_detail2.html', {
        "output_id": outputmary.output_id,
        "pw_product": outputmary.pw_product,
        "merchant_name": outputmary.merchant_name,
        "merchant_id": outputmary.merchant_id,
        "project_name": outputmary.project_name,
        "project_id": outputmary.project_id,
        "merchant_url": outputmary.merchant_url,
        "url": outputmary.url,
        "scan_time": outputmary.scan_time,
        "page_content": outputmary.page_content,
        "keyword_matched": outputmary.keyword_matched,
        "screenshot_dir": outputmary.screenshot_dir,
        "keywords": outputmary.input_id.keywords,
        "keyword_logic": outputmary.input_id.keyword_logic,
    })
